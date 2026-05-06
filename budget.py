import pandas as pd
from database import get_connection

def set_budget(user_id, category, limit):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO budgets(user_id, category, limit_amount)
    VALUES (?, ?, ?)
    """, (user_id, category, limit))

    conn.commit()
    conn.close()

def check_budget(user_id):
    conn = get_connection()

    expenses = pd.read_sql("""
    SELECT category, SUM(amount) as total
    FROM expenses
    WHERE user_id=?
    GROUP BY category
    """, conn, params=(user_id,))

    budgets = pd.read_sql("""
    SELECT category, limit_amount
    FROM budgets
    WHERE user_id=?
    """, conn, params=(user_id,))

    conn.close()

    if expenses.empty or budgets.empty:
        return pd.DataFrame()

    merged = expenses.merge(budgets, on="category")
    merged["alert"] = merged["total"] > merged["limit_amount"]

    return merged