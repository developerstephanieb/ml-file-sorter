import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns


FILE = "data/ia_files.csv"
categories = ['gutenberg', 'softwarelibrary_msdos', 'folkscanomy']

def main():
    df = pd.read_csv("data/ia_files.csv")

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
    best_model = None
    best_f1 = 0.0
    best_accuracy = 0.0
    for name, algo in test_algorithems.items():
        model = Pipeline([
            ('tfidf', TfidfVectorizer()), 
            ('clf', algo)
        ])
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        f1 = f1_score(y_test, y_pred, average='weighted')
        best_accuracy  = accuracy_score(y_test, y_pred)
        if f1 > best_f1:
            best_f1 = f1
            best_model = algo
            best_accuracy = accuracy_score

        
        
        print(f"{name} F1 Score: {f1:.4f}")
        print(classification_report(y_test, y_pred, target_names=categories))
        cm = confusion_matrix(y_test, y_pred, labels=categories)
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=categories, yticklabels=categories)
        plt.title(f'Confusion Matrix for {name}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.show()
    
    print(f"Best Model: {best_model.__class__.__name__} with accuaracy: {best_accuracy:.4f}")
    print('_' * 50)

    df = pd.read_csv(FILE)

    X = df['file_name']
    y = df['category']

    model = Pipeline([
       ('tfidf', TfidfVectorizer()),
       ('clf', best_model)  # Use the best model or default to MultinomialNB
    ])

    model.fit(X, y)

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, "model/classifier.pkl")

    print("Model trained and saved to model/classifier.pkl")

if __name__ == "__main__":
    main()