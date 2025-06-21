import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

df = pd.read_csv("data/labeled_files.csv")

X = df['file_name']
y = df['category']

model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

model.fit(X, y)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/classifier.pkl")

print("Model trained and saved to model/classifier.pkl")
