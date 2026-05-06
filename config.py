import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "expenses.db")

# Ensure DB folder exists
os.makedirs(os.path.join(BASE_DIR, "db"), exist_ok=True)