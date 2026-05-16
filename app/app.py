from flask import Flask, render_template, request, jsonify
from utils.email_check import predict_email
from utils.url_check import analyze_url
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# ========== EMAIL DETECTION ROUTES ==========

@app.route("/email")
def email_page():
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
        timestamp = datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
        detection_type = "email"
    )

# ========== URL DETECTION ROUTES ==========

@app.route("/url")
def url_page():
    return render_template("url.html")

@app.route("/predict_url", methods=["POST"])
def predict_url_route():
    url_text = request.form.get("url", "").strip()

    if not url_text:
        return render_template(
            "url.html",
            error="Please enter a URL before scanning."
        )

    result = analyze_url(url_text)

    return render_template(
        "url_result.html",
        label       = result["label"],
        risk        = result["risk"],
        score       = result["score"],
        url         = result.get("url", url_text),
        threats     = result.get("threats", []),
        timestamp   = datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
        detection_type = "url"
    )

# ========== API ENDPOINTS (JSON RESPONSES) ==========

@app.route("/api/analyze_email", methods=["POST"])
def api_analyze_email():
    """API endpoint for email analysis (returns JSON)"""
    data = request.get_json()
    email_text = data.get("email", "").strip()
    
    if not email_text:
        return jsonify({"error": "Email content required"}), 400
    
    result = predict_email(email_text)
    return jsonify(result)

@app.route("/api/analyze_url", methods=["POST"])
def api_analyze_url():
    """API endpoint for URL analysis (returns JSON)"""
    data = request.get_json()
    url_text = data.get("url", "").strip()
    
    if not url_text:
        return jsonify({"error": "URL required"}), 400
    
    result = analyze_url(url_text)
    return jsonify(result)

# ========== DASHBOARD ROUTE ==========

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ========== ERROR HANDLERS ==========

@app.errorhandler(500)
def server_error(e):
    return render_template("email.html", error="Something went wrong. Please try again."), 500

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html", error="Page not found."), 404

if __name__ == "__main__":
    app.run(debug=True)
