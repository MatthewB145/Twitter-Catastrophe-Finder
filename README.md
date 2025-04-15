Project Proposal: Twitter Catastrophe Finder

Project Team:
Matthew Bierie - Team Lead
Gerardo Rios - Scrum Master
Elizaveta Filonova - Software Engineer
Faizan-Ali Lalani - Data Engineer

Project Overview:
The Twitter Catastrophe Finder aims to detect emerging crisis situations using real-time Twitter data. By leveraging the Tweepy library for data collection, Scikit-learn for machine learning-based classification, and Flask for a user-friendly web dashboard, this project will help first responders and analysts identify potential disasters as they unfold.

Objectives
Develop an automated system to collect real-time Twitter data related to disasters.
Implement natural language processing (NLP) techniques to classify tweets as catastrophic or non-catastrophic.
Provide a Flask-based web interface for visualization and alerts as well as easy to read graphics and maps.
Ensure a user friendly interface that is intuitive and easy to use.

Project Phases
Data Collection Module
Authenticate with Twitter API using Tweepy.
Stream tweets using relevant keywords and geolocation filters.
Store raw tweets in a database.
Preprocessing & Feature Extraction
Tokenization, stopword removal, and stemming using NLTK/Spacy.
Feature extraction using TF-IDF or word embeddings.
Machine Learning Model
Train a classifier (e.g., logistic regression, SVM, or deep learning model) using labeled disaster-related tweets.
Evaluate the model’s performance using accuracy, precision, and recall.
Web Dashboard
Develop a Flask-based front-end with visual analytics.
Provide real-time alerts and summary statistics.
Deployment & Optimization
Deploy on cloud or local server.
Optimize for scalability and performance.

Estimated Costs:
Twitter Api Access - $100 a month
AWS Cloud Hosting - $14 a month
Database Costs - $15 a month
Domain and SSL certificate - $10 a month

Risks & Challenges
API Limitations: Twitter API rate limits may restrict data collection speed and costs for real time streaming may become large.
Data Bias: The accuracy of classification depends on high-quality training data.
Scalability: Processing large volumes of tweets in real time may require cloud-based solutions.
False Positives: Ensuring model reliability to reduce misclassification.

 Expected Outcomes
A functional web-based tool capable of detecting potential disasters using Twitter.
A trained machine learning model with high accuracy for catastrophe detection.
A scalable and deployable system for real-world application.

Conclusion:
 This project will provide a valuable tool for detecting disasters early using social media data, allowing authorities and emergency responders to act swiftly. By leveraging machine learning and web technologies, the Twitter Catastrophe Finder will be a step forward in real-time crisis monitoring.


