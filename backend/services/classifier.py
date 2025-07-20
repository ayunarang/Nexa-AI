import joblib
from utils.text_utils import clean_text

clf = joblib.load("label_classifier_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def classify_chunks(chunks):
    texts = [clean_text(chunk["text"]) for chunk in chunks]
    X_tfidf = vectorizer.transform(texts)
    predictions = clf.predict(X_tfidf)

    return [
        {
            "label": label,
            "start": chunk["start"],
            "end": chunk["end"],
            "text": chunk["text"]
        }
        for chunk, label in zip(chunks, predictions)
    ]
