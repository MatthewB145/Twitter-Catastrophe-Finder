# train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import SVC
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
    df = pd.read_csv('train.csv')
    df = df.dropna(subset=['text', 'target', 'disaster_type'])
    df['processed_text'] = df['text'].apply(preprocess_text)

    X = df['processed_text']
    le_disaster = LabelEncoder()
    disaster_types_encoded = le_disaster.fit_transform(df['disaster_type'])
    df['target'] = df['target'].astype(int)
    y = np.column_stack((df['target'], disaster_types_encoded))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_vectorized = vectorizer.fit_transform(X_train)

    clf = SVC(C=1, kernel='linear', probability=True, random_state=42)
    multi_classifier = MultiOutputClassifier(clf)
    multi_classifier.fit(X_train_vectorized, y_train)

    # Save the model, vectorizer, and encoder
    joblib.dump(multi_classifier, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(le_disaster, 'label_encoder.pkl')

    print("Model, vectorizer, and label encoder saved.")

if __name__ == "__main__":
    main()