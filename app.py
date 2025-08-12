from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import joblib

app = Flask(__name__)
app.secret_key = "yoursecretkey"  # Needed for session handling
CORS(app)  # Enable CORS for all routes

# Load trained model
model = joblib.load("illness_model.pkl")

# Feature order (must match training)
features = [
    "fever",
    "cough",
    "headache",
    "fatigue",
    "sore_throat",
    "vomiting",
    "rash",
    "diarrhea",
    "shortness_of_breath",
    "chest_pain"
]

# ===== LOGIN PAGE =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Example static login (you can replace with DB check)
        if username == "admin" and password == "password":
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ===== FORM PAGE =====
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


# ===== RESULT PAGE =====
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))

    symptoms = request.form.getlist("symptoms")

    # Normalize input
    input_symptoms = [s.lower().replace(" ", "_") for s in symptoms]
    input_features = [1 if feature in input_symptoms else 0 for feature in features]

    # Prediction
    prediction = model.predict([input_features])[0]

    return render_template("result.html", diagnosis=prediction)


# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)






