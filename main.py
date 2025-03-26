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
            "tsunami"
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
        feed_uris = [
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejsyozb6iq', #Fire
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejwgffwqky', #Hurricane
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejxlobe474', #Earthquake
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejy45orees', #Tornado
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejqjms3noe' #Flood
        ]
        # Fetch posts from the user's feed
        for uri in feed_uris:
            feed = client.app.bsky.feed.get_feed({'feed': uri, 'limit': 10})

            # Process posts
            for post in feed.feed:
                # Check if post contains any disaster-related terms
                post_text = post.post.record.text.lower()

                # Check if any search term is in the post
                if any(term.lower() in post_text for term in search_terms):
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



    bluesky_username = "matthewb145.bsky.social"
    bluesky_password = "Familypets4"

    disaster_posts = fetch_disaster_related_posts(
        bluesky_username,
        bluesky_password,
        days_back=3
    )

    # Predict disaster type for fetched posts
    bluesky_results = {
        'predictions': []
    }

    for post in disaster_posts:
        is_disaster, disaster_type = predict_disaster(post['text'])

        result = {
            'text': post['text'],
            'author': post['author'],
            'created_at': post['created_at'],
            'is_disaster': is_disaster,
            'disaster_type': disaster_type
        }
        bluesky_results['predictions'].append(result)

    save_to_json(bluesky_results, 'bluesky_prediction_results.json')
    if mongo_client: save_to_mongodb(mongo_client, 'bluesky_db', 'Cleaned_Data', bluesky_results)
if __name__ == "__main__":
    main()

