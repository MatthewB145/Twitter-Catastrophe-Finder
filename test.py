import pandas as pd
import re
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet", quiet=True)
lemmatizer = WordNetLemmatizer()


df = pd.read_csv("train.csv")

df = df.dropna(subset=['target', 'Severity', 'disaster_type'])


nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))


def clean_text(text):
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower().strip()
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)


df["clean_text"] = df["text"].apply(clean_text)
df['combined_label'] = df['Severity'] + "_" + df['disaster_type']

y = df["combined_label"]


vectorizer_configs = {
    "Default": TfidfVectorizer(),
    "Max Features (5000)": TfidfVectorizer(max_features=5000),
    "Min-Max DF (2, 0.9)": TfidfVectorizer(min_df=2, max_df=0.9),
    "Bigrams": TfidfVectorizer(ngram_range=(1, 2)),
    "Remove Stopwords": TfidfVectorizer(stop_words="english"),
    "Sublinear TF": TfidfVectorizer(sublinear_tf=True),
}

results = {}

for name, vectorizer in vectorizer_configs.items():
    print(f"Testing: {name}")

    X = vectorizer.fit_transform(df["clean_text"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    clf = SVC(kernel="linear")
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    results[name] = accuracy

    print(f"Accuracy: {accuracy}\n")

# Print all results
for config, acc in results.items():
    print(f"{config}: {acc:.4f}")





X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)


clf = SVC(kernel="linear")
clf.fit(X_train, y_train)


y_pred = clf.predict(X_test)


print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))



new_tweet = ["I'm Dying and I need help from an Ambulance!"]
X_new = vectorizer.transform(new_tweet)
predicted_label = clf.predict(X_new)[0]
severity, disaster_type = predicted_label.split("_")

print(f"Predicted Severity: {severity}")
print(f"Predicted Disaster Type: {disaster_type}")


new_tweet_2 = ["The building is on fire!"]
X_new_2 = vectorizer.transform(new_tweet_2)
predicted_label_2 = clf.predict(X_new_2)[0]
severity_2, disaster_type_2 = predicted_label_2.split("_")

print(f"Predicted Severity: {severity_2}")
print(f"Predicted Disaster Type: {disaster_type_2}")

new_tweet_3 = ["It is a beautiful day outside today. My legs are on fire"]
X_new_3 = vectorizer.transform(new_tweet_3)
predicted_label_3 = clf.predict(X_new_3)[0]
severity_3, disaster_type_3 = predicted_label_3.split("_")

print(f"Predicted Severity: {severity_3}")
print(f"Predicted Disaster Type: {disaster_type_3}")
