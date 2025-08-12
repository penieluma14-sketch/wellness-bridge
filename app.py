from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import joblib

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session management
CORS(app)

# Load Cholera model
model = joblib.load("cholera_model.pkl")

# Symptoms used for Cholera detection
features = ["fever", "diarrhea", "vomiting", "dehydration"]

# Simple login credentials
USERNAME = "admin"
PASSWORD = "password"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == USERNAME and password == PASSWORD:
        session["logged_in"] = True
        return redirect(url_for("home"))
    else:
        return "❌ Invalid username or password. <a href='/'>Try again</a>"

@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = request.get_json()
    input_symptoms = [s.lower().replace(" ", "_") for s in data["symptoms"]]
    input_features = [1 if feature in input_symptoms else 0 for feature in features]

    prediction = model.predict([input_features])[0]

    diagnosis = "Cholera detected" if prediction == 1 else "No Cholera detected"
    return jsonify({"diagnosis": diagnosis})

@app.route("/result")
def result():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)








