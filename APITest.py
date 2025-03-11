
#Faizan-Ali Lalani
#FBL230000


from pymongo import MongoClient
from atproto import Client


# Disaster keywords
disaster_keywords = ["earthquake", "flood", "hurricane", "fire", "tsunami", "tornado", "disaster", "emergency"]

# Connect to MongoDB
client_mongo = MongoClient("mongodb+srv://Twitterdb:<password>@cluster0.toqut.mongodb.net/")

database = client_mongo["bluesky_db"]
collection = database["disaster_feed"]

# Connect to Bluesky API
client_bsky = Client()

# Enter Bluesky user and password 
client_bsky.login('bluesky-login', 'password')

# Get All of Bluesky Posts
feed = client_bsky.app.bsky.feed.get_timeline()

# Filter out disaster-related posts, based on the text 
for post in feed['feed']:
    #record = post.get('record', {}) ??
    #content_text = record.get('text', '').lower() ??
    content_text = post['record']['text'].lower()

# Filter for disaster based on keywords
    if any(keyword in content_text for keyword in disaster_keywords):  
        data = {
            "post_id": post['uri'],
            #"author": post['author']['handle'], (If needed)
            "location": post.get('location', 'Unknown'),
            "content": post['record']['text'],
            #"created_at": post['record']['createdAt'] (If Needed)
        }
        # Prevent duplicates
        collection.update_one({"post_id": data["post_id"]}, {"$set": data}, upsert=True)  

print("Disaster feed updated successfully.")
