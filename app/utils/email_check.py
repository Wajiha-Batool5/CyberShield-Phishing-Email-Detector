import joblib

# load trained model
model = joblib.load("models/phishing_svm_model.joblib")
# load TF-IDF vectorizer
vectorizer = joblib.load("models/phishing_tfidf_vectorizer.joblib")

def predict_email(email_text):
    # preprocess email text
    email_vector = vectorizer.transform([email_text])

    # predict using the loaded model
    prediction = model.predict(email_vector)[0]

    score = model.decision_function(email_vector)[0]

    # Convert score into 0–100 range
    phishing_score = int((score + 1) * 50)

    # Keep score between 0 and 100
    phishing_score = max(0, min(phishing_score, 100))

    # Risk Scoring Logic
    if phishing_score <= 40:
        risk = "LOW"
        label = "SAFE"

    elif phishing_score <= 70:
        risk = "MEDIUM"
        label = "SUSPICIOUS"

    else:
        risk = "HIGH"
        label = "PHISHING"


    return {
        "label": label,
        "risk": risk,
        "score": phishing_score
    }