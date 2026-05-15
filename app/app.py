from flask import Flask, render_template, request, jsonify
from utils.email_check import predict_email
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("email.html")

@app.route("/predict_email", methods=["POST"])
def predict_email_route():
    email_text = request.form.get("email", "").strip()

    if not email_text:
        return render_template(
            "email.html",
            error="Please paste some email content before scanning."
        )

    result = predict_email(email_text)

    return render_template(
        "result.html",
        label     = result["label"],
        risk      = result["risk"],
        score     = result["score"],
        email     = email_text,
        timestamp = datetime.datetime.now().strftime("%d %b %Y, %H:%M")
    )

@app.errorhandler(500)
def server_error(e):
    return render_template("email.html", error="Something went wrong. Please try again."), 500

if __name__ == "__main__":
    app.run(debug=True)