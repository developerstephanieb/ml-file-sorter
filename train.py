import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

import numpy as np
import joblib
import os
import time

df = pd.read_csv("data/labeled_files.csv")

X = df['file_name']
y = df['category']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

test_algorithems = {
    'MultinomialNB': MultinomialNB(),
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(),
    'SVC_linear': SVC(kernel='linear'),
    'LogisticRegression': LogisticRegression(max_iter=1000,random_state=42),
    'KNeighbors': KNeighborsClassifier(n_neighbors=5)
}

trained_models = {}
print("Training individual models...")
print('_' * 50)

for name, algo in test_algorithems.items():
    start_time = time.time()
    model = Pipeline([
        ('tfidf', TfidfVectorizer()), 
        ('clf', algo)
    ])
    model.fit(x_train, y_train)
    end_time = time.time()
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"{name} trained in {end_time - start_time} seconds")
    print(f"{name} accuracy: {accuracy:.5f}")

# os.makedirs("model", exist_ok=True)
# joblib.dump(model, "model/classifier.pkl")

# print("Model trained and saved to model/classifier.pkl")
