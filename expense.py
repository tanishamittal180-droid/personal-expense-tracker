from database import get_connection

def add_expense(user_id, date, desc, amount, category):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO expenses(user_id, date, description, amount, category)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, desc, amount, category))

    conn.commit()
    conn.close()