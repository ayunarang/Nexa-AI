import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import joblib
import numpy as np

df = pd.read_csv("labeledTranscripts.csv")
df['text'] = df['text'].astype(str).str.strip().str.strip('"')

X = df['text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=5000,
    sublinear_tf=True,
    strip_accents='unicode',
    dtype=np.float32
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

clf = LinearSVC()
clf.fit(X_train_tfidf, y_train)

y_pred = clf.predict(X_test_tfidf)
print("Classification Report:\n")
print(classification_report(y_test, y_pred))

joblib.dump(clf, "label_classifier_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
