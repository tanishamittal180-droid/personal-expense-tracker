import pandas as pd
from database import get_connection

def get_user_data(user_id):
    conn = get_connection()

    df = pd.read_sql("""
    SELECT date, category, amount
    FROM expenses
    WHERE user_id=?
    """, conn, params=(user_id,))

    conn.close()
    return df