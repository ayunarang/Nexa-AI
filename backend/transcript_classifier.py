import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv("labeledTranscripts.csv")

# Ensure text is string type
df['text'] = df['text'].astype(str)

# Strip leading/trailing whitespace and quotes
df['text'] = df['text'].str.strip().str.strip('"')

# Add double quotes around each entry
df['text'] = '"' + df['text'] + '"'

# Split into X and y
X = df['text']
y = df['label']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the classifier
clf = LinearSVC()
clf.fit(X_train_tfidf, y_train)

# Evaluate
y_pred = clf.predict(X_test_tfidf)
print("Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save the model and vectorizer
joblib.dump(clf, "label_classifier_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
