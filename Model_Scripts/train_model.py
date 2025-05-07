# train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
import re
import joblib


def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    return re.sub(r'[^a-zA-Z\s]', '', text)


def main():
    # Load and preprocess data
    df = pd.read_csv('train3_modified.csv')
    df = df.dropna(subset=['text', 'disaster_type'])
    df['processed_text'] = df['text'].apply(preprocess_text)

    X = df['processed_text']
    le_disaster = LabelEncoder()
    y = le_disaster.fit_transform(df['disaster_type'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', max_df=0.75, min_df=2, ngram_range=(1, 2))
    X_train_vectorized = vectorizer.fit_transform(X_train)

    # Changed to LinearSVC with specified parameters
    clf = LinearSVC(
        C=1,
        class_weight='balanced',
        dual=True,
        loss='hinge',
        max_iter=1000,
        penalty='l2',
        random_state=42,
        tol=0.0001
    )

    clf.fit(X_train_vectorized, y_train)

    # Save the model, vectorizer, and encoder
    joblib.dump(clf, 'Help/model.pkl')
    joblib.dump(vectorizer, 'Help/vectorizer.pkl')
    joblib.dump(le_disaster, 'Help/label_encoder.pkl')

    print("Model, vectorizer, and label encoder saved.")


if __name__ == "__main__":
    main()