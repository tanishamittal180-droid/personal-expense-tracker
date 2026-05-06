import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
from database import get_connection

MODEL_PATH = "models/model.pkl"

def train_model():
    conn = get_connection()

    df = pd.read_sql("""
    SELECT description, category FROM expenses
    """, conn)

    conn.close()

    if df.empty:
        print("No data to train")
        return

    X = df["description"]
    y = df["category"]

    vec = CountVectorizer()
    X_vec = vec.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vec, y)

    joblib.dump((model, vec), MODEL_PATH)
    print("Model trained")

def predict_category(desc):
    model, vec = joblib.load(MODEL_PATH)
    return model.predict(vec.transform([desc]))[0]