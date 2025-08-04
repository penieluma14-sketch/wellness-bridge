from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load trained model
model = joblib.load("illness_model.pkl")

# Define feature order (must match training)
features = ["fever", "cough", "headache", "nausea"]

# Home route – serves the HTML page
@app.route("/")
def home():
    return render_template("index.html")

# API endpoint for predictions
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Convert symptoms into binary feature list
    input_features = [1 if symptom in data["symptoms"] else 0 for symptom in features]

    # Predict using model
    prediction = model.predict([input_features])[0]

    return jsonify({"diagnosis": prediction})

# Run locally
if __name__ == "__main__":
    app.run(debug=True)

