from flask import Flask, render_template, request
import joblib
from feature_extraction import extract_features
import csv, os
from datetime import datetime

app = Flask(__name__)

model = joblib.load("model/phishing_model.pkl")
REPORT_PATH = "reports/predictions.csv"


@app.route("/")
def dashboard():
    total = phishing = legit = 0

    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                if row["Result"] == "Phishing":
                    phishing += 1
                else:
                    legit += 1

    accuracy = round((legit / total) * 100, 2) if total else 0

    return render_template(
        "dashboard.html",
        total=total,
        phishing=phishing,
        legit=legit,
        accuracy=accuracy
    )


@app.route("/scan", methods=["GET", "POST"])
def scan():
    prediction = confidence = None

    if request.method == "POST":
        url = request.form["url"]
        features = extract_features(url)

        probs = model.predict_proba([features])[0]
        result = model.predict([features])[0]

        if result == 1:
            prediction = "Phishing"
            confidence = round(probs[1] * 100, 2)
        else:
            prediction = "Legitimate"
            confidence = round(probs[0] * 100, 2)

        os.makedirs("reports", exist_ok=True)
        file_exists = os.path.isfile(REPORT_PATH)

        with open(REPORT_PATH, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Time", "URL", "Result", "Confidence"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                url, prediction, confidence
            ])

    return render_template("scan.html", prediction=prediction, confidence=confidence)


@app.route("/reports")
def reports():
    data = []
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH) as f:
            reader = csv.DictReader(f)
            data = list(reader)

    return render_template("reports.html", data=data)


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True)
