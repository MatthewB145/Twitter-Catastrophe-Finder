import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import re
import json
import pymongo
from pymongo import MongoClient
import requests
import os
from atproto import Client, models
from datetime import datetime, timedelta
from sklearn.svm import SVC

# MongoDB Connection Functions
def get_mongodb_connection(connection_string):
    try:
        client = MongoClient(connection_string)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def save_to_mongodb(client, database_name, collection_name, data):
    try:
        db = client['bluesky_db']
        collection = db['Cleaned_Data']

        if isinstance(data, list):
            collection.insert_many(data)
        elif isinstance(data, dict):
            collection.insert_one(data)

        print(f"Data saved to {'bluesky_db'}.{'Cleaned_Data'}")
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")


def load_from_mongodb(client, database_name, collection_name):
    try:
        db = client["bluesky_db"]
        collection = db["Cleaned_Data"]

        data = list(collection.find())

        return data
    except Exception as e:
        print(f"Error loading from MongoDB: {e}")
        return None


# JSON Handling Functions
def save_to_json(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")


def load_from_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading from JSON: {e}")
        return None


# Bluesky Post Fetching Function
def fetch_disaster_related_posts(username, password, search_terms=None, days_back=7):
    """
    Fetch disaster-related posts from Bluesky using AT Protocol

    Args:
        username (str): Bluesky account username
        password (str): Bluesky account password
        search_terms (list, optional): List of disaster-related search terms.
                                       Defaults to a predefined list if None.
        days_back (int, optional): Number of days to look back. Defaults to 7.

    Returns:
        list: A list of disaster-related posts
    """
    # Default search terms if not provided
    if search_terms is None:
        search_terms = [
            "disaster",
            "emergency",
            "earthquake",
            "hurricane",
            "flood",
            "wildfire",
            "tornado",
            "tsunami",
            "crisis"
        ]

    try:
        # Initialize Bluesky client
        client = Client()
        client.login(username, password)

        # Calculate the date range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days_back)

        # Collect posts
        disaster_posts = []

        # Fetch posts from the user's feed
        feed = client.get_timeline(limit=100)

        # Process posts
        for post in feed.feed:
            # Check if post contains any disaster-related terms
            post_text = post.post.record.text.lower()

            # Check if any search term is in the post
            if 1==1:
                processed_post = {
                    'text': post.post.record.text,
                    'created_at': post.post.record.created_at,
                    'author': post.post.author.handle,
                    'uri': post.post.uri
                }
                disaster_posts.append(processed_post)

        return disaster_posts

    except Exception as e:
        print(f"Error fetching disaster-related posts: {e}")
        return []
# Load and preprocess the data
def preprocess_text(text):
    # Handle NaN values
    if pd.isna(text):
        return ""
    # Convert to string if not already
    text = str(text)
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


def main():
    # MongoDB Connection String
    connection_string = "mongodb+srv://Twitterdb:CS4485.0W1@cluster0.toqut.mongodb.net/"

    # Connect to MongoDB
    mongo_client = get_mongodb_connection(connection_string)

    # Load the dataset
    df = pd.read_csv('train.csv')

    # Remove rows with NaN values in important columns
    df = df.dropna(subset=['text', 'target', 'disaster_type'])

    # Preprocess the text
    df['processed_text'] = df['text'].apply(preprocess_text)

    # Prepare features (X) and targets (y)
    X = df['processed_text']

    # Encode target and disaster_type
    le_disaster = LabelEncoder()
    disaster_types_encoded = le_disaster.fit_transform(df['disaster_type'])

    # Convert target to int
    df['target'] = df['target'].astype(int)

    # Create multi-target array
    y = np.column_stack((df['target'], disaster_types_encoded))

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Create and train the multi-output classifier
    rf_classifier = SVC(C=1, kernel='linear', probability=True, random_state=42)
    multi_target_classifier = MultiOutputClassifier(rf_classifier)
    multi_target_classifier.fit(X_train_vectorized, y_train)

    # Make predictions
    predictions = multi_target_classifier.predict(X_test_vectorized)

    # Print classification reports
    print("Target (Disaster/Non-disaster) Classification Report:")
    print(classification_report(y_test[:, 0], predictions[:, 0]))

    print("\nDisaster Type Classification Report:")
    print(classification_report(y_test[:, 1], predictions[:, 1]))

    # Function to make predictions on new text
    def predict_disaster(text):
        try:
            # Preprocess the text
            processed = preprocess_text(text)
            # Vectorize the text
            vectorized = vectorizer.transform([processed])
            # Make prediction
            prediction = multi_target_classifier.predict(vectorized)[0]

            # Convert predictions to proper types
            is_disaster = "Disaster" if int(prediction[0]) == 1 else "Not a disaster"
            disaster_type = le_disaster.inverse_transform([int(prediction[1])])[0]

            return is_disaster, disaster_type
        except Exception as e:
            print(f"Error in prediction: {e}")
            return "Unknown", "Unknown"

    # Print unique disaster types for verification
    print("\nUnique disaster types in training data:")
    print(le_disaster.classes_)

    # Fetch disaster-related posts from Bluesky
    bluesky_username = "matthewb145.bsky.social"  # Replace with actual username
    bluesky_password = "Familypets4"  # Replace with actual password

    disaster_posts = fetch_disaster_related_posts(
        bluesky_username,
        bluesky_password,
        days_back=3  # Look back 3 days
    )

    #Save fetched posts to MongoDB
    if mongo_client:
        save_to_mongodb(mongo_client, 'bluesky_db', 'Test', disaster_posts)

    # Predict disaster type for fetched posts
    bluesky_results = {
        'predictions': [],
        'posts': disaster_posts
    }

    print("\nPredictions for Bluesky posts:")
    for post in disaster_posts:
        is_disaster, disaster_type = predict_disaster(post['text'])
        print(f"\nPost by {post['author']}: {post['text']}")
        print(f"Prediction: {is_disaster}")
        print(f"Disaster Type: {disaster_type}")

        # Store results
        result = {
            'text': post['text'],
            'author': post['author'],
            'created_at': post['created_at'],
            'is_disaster': is_disaster,
            'disaster_type': disaster_type
        }
        bluesky_results['predictions'].append(result)

    # Save Bluesky results to JSON
    save_to_json(bluesky_results, 'bluesky_prediction_results.json')
'''
    # Example usage with sample texts (kept from previous version)
    sample_texts = [
        "A huge forest fire has broken out in California",
        "I love the way the sun sets in the evening",
        "Earthquake magnitude 7.2 hits Japan coast"
    ]

    # Prepare results for saving
    results = {
        'predictions': [],
        'sample_texts': sample_texts
    }

    print("\nPredictions for sample texts:")
    for text in sample_texts:
        is_disaster, disaster_type = predict_disaster(text)
        print(f"\nText: {text}")
        print(f"Prediction: {is_disaster}")
        print(f"Disaster Type: {disaster_type}")

        # Store results
        result = {
            'text': text,
            'is_disaster': is_disaster,
            'disaster_type': disaster_type
        }
        results['predictions'].append(result)

    # Save results to MongoDB
    if mongo_client:
        save_to_mongodb(mongo_client, 'bluesky_db', 'Cleaned_Data', results)

    # Save results to JSON
    save_to_json(results, 'prediction_results.json')

    # Print final results
    print("\nFinal Prediction Results:")
    print(json.dumps(results, indent=2))
'''

if __name__ == "__main__":
    main()
