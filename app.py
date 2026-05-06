import streamlit as st
import pandas as pd
from database import init_db
from auth import create_user, login_user
from expense import add_expense
from analyze import get_user_data
from budget import set_budget, check_budget

# ---------------- INIT ----------------
init_db()

st.set_page_config(page_title="Expense Tracker", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {background-color: #f5f7fa;}
.card {
    padding:20px;
    border-radius:15px;
    background-color:white;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    text-align:center;
}
.title {
    text-align:center;
    font-size:36px;
    font-weight:bold;
    color:#4CAF50;
}
.subtitle {
    text-align:center;
    color:gray;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">💸 Personal Expense Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Track • Analyze • Save Money</div>', unsafe_allow_html=True)

# ---------------- AUTH ----------------
menu = st.sidebar.selectbox("Menu", ["Login", "Signup"], key="menu")

if menu == "Signup":
    st.subheader("Create Account")
    user = st.text_input("Username", key="signup_user")
    pwd = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Sign Up", key="signup_btn"):
        if create_user(user, pwd):
            st.success("Account created successfully")
        else:
            st.error("User already exists")

elif menu == "Login":
    st.subheader("Login")
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        result = login_user(user, pwd)
        if result:
            st.session_state["user_id"] = result[0]
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ---------------- MAIN DASHBOARD ----------------
if "user_id" in st.session_state:

    user_id = st.session_state["user_id"]

    st.sidebar.success("Logged in")

    df = get_user_data(user_id)

    # ---------------- KPI CARDS ----------------
    if not df.empty:
        total = int(df["amount"].sum())
        avg = int(df["amount"].mean())
        max_val = int(df["amount"].max())

        c1, c2, c3 = st.columns(3)

        c1.markdown(f"<div class='card'><h3>Total Spend</h3><h2>₹{total}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='card'><h3>Average Spend</h3><h2>₹{avg}</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='card'><h3>Max Spend</h3><h2>₹{max_val}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- ADD EXPENSE ----------------
    st.subheader("➕ Add New Expense")

    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Date", key="date")

    with col2:
        amount = st.number_input("Amount", key="amount")

    with col3:
        category = st.selectbox(
            "Category",
            ["Food", "Travel", "Bills", "Shopping"],
            key="expense_category"
        )

    desc = st.text_input("Description", key="desc")

    if st.button("Add Expense", key="add_btn"):
        add_expense(user_id, str(date), desc, amount, category)
        st.success("Expense added successfully")

    st.markdown("---")

    # ---------------- CHARTS ----------------
    if not df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Category Spending")
            st.bar_chart(df.groupby("category")["amount"].sum())

        with col2:
            st.subheader("📈 Daily Trend")
            st.line_chart(df.groupby("date")["amount"].sum())

    st.markdown("---")

    # ---------------- BUDGET ----------------
    st.subheader("💰 Budget Management")

    col1, col2 = st.columns(2)

    with col1:
        bcat = st.selectbox(
            "Select Category",
            ["Food", "Travel", "Bills", "Shopping"],
            key="budget_category"
        )

    with col2:
        limit = st.number_input("Set Limit", key="limit")

    if st.button("Set Budget", key="budget_btn"):
        set_budget(user_id, bcat, limit)
        st.success("Budget saved")

    # ---------------- ALERTS ----------------
    st.subheader("🚨 Budget Alerts")

    alerts = check_budget(user_id)

    if not alerts.empty:
        st.dataframe(alerts)
    else:
        st.info("No alerts — you're within budget 👍")

    st.markdown("---")

    # ---------------- DATA TABLE ----------------
    st.subheader("📄 Transaction History")
    st.dataframe(df)