# classify_posts.py

import joblib
import re
import json
from datetime import datetime
import ssl
import certifi
from atproto import Client
from geopy.geocoders import Nominatim
from pymongo import MongoClient

context = ssl.create_default_context(cafile=certifi.where())

def preprocess_text(text):
    if not text:
        return ""
    text = str(text).lower()
    return re.sub(r'[^a-zA-Z\s]', '', text)

def load_names(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return {line.strip().lower() for line in file if line.strip()}

def extract_location(text, filename='Final_List.txt'):
    cities = load_names(filename)
    found = [city for city in cities if re.search(r'\b' + re.escape(city) + r'\b', text.lower())]
    return found

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="city_coordinates_extractor", ssl_context=context)
    location = geolocator.geocode(city_name, timeout=30)
    if location:
        return location.latitude, location.longitude
    return None

def fetch_disaster_related_posts(username, password, search_terms=None, days_back=3):
    if search_terms is None:
        search_terms = ["disaster", "emergency", "earthquake", "hurricane", "flood", "wildfire", "tornado", "tsunami"]

    try:
        client = Client()
        client.login(username, password)

        feed_uris = [
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejsyozb6iq',
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejwgffwqky',
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejxlobe474',
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejy45orees',
            'at://did:plc:qiknc4t5rq7yngvz7g4aezq7/app.bsky.feed.generator/aaaejqjms3noe'
        ]

        posts = []
        for uri in feed_uris:
            feed = client.app.bsky.feed.get_feed({'feed': uri, 'limit': 10})
            for post in feed.feed:
                text = post.post.record.text.lower()
                if any(term in text for term in search_terms):
                    posts.append({
                        'text': post.post.record.text,
                        'created_at': post.post.record.created_at,
                        'author': post.post.author.handle,
                        'uri': post.post.uri
                    })
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

def save_to_mongodb(client, data):
    try:
        db = client['bluesky_db']
        collection = db['Cleaned_Data']
        collection.insert_many(data['predictions'])
        print("Saved to MongoDB.")
    except Exception as e:
        print(f"MongoDB error: {e}")

def main():
    # Load model, vectorizer, and label encoder
    try:
        clf = joblib.load('model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        label_encoder = joblib.load('label_encoder.pkl')
    except Exception as e:
        print("Model files not found. Run `train_model.py` first.")
        return

    def predict_disaster(text):
        processed = preprocess_text(text)
        vectorized = vectorizer.transform([processed])
        prediction = clf.predict(vectorized)[0]
        is_disaster = "Disaster" if int(prediction[0]) == 1 else "Not a disaster"
        disaster_type = label_encoder.inverse_transform([int(prediction[1])])[0]
        return is_disaster, disaster_type

    username = "matthewb145.bsky.social"
    password = "Familypets4"
    posts = fetch_disaster_related_posts(username, password, days_back=3)

    results = {'predictions': []}
    for post in posts:
        is_disaster, disaster_type = predict_disaster(post['text'])
        found_cities = extract_location(post['text'])
        locations = []

        if found_cities:
            coords = get_coordinates(found_cities[0].title())
            if coords:
                locations.append({'city': found_cities[0].title(), 'latitude': coords[0], 'longitude': coords[1]})

        results['predictions'].append({
            'name': disaster_type,
            'location': locations[0]['city'] if locations else '',
            'latitude': locations[0]['latitude'] if locations else '',
            'longitude': locations[0]['longitude'] if locations else '',
            'report': post['text'],
            'disaster_level': is_disaster,
            'date': post['created_at'][:10]
        })

    with open('bluesky_prediction_results.json', 'w') as f:
        json.dump(results, f, indent=4)

    # Save to MongoDB
    try:
        mongo_client = MongoClient("mongodb+srv://Twitterdb:CS4485.0W1@cluster0.toqut.mongodb.net/")
        save_to_mongodb(mongo_client, results)
    except Exception as e:
        print("MongoDB connection error.")

if __name__ == "__main__":
    main()