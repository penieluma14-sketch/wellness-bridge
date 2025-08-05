from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib

app = Flask(__name__)
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


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Generate feature vector in the same order as training
    input_features = [1 if symptom in data["symptoms"] else 0 for symptom in features]

    prediction = model.predict([input_features])[0]
    return jsonify({"diagnosis": prediction})


if __name__ == "__main__":
    app.run(debug=True)  # Local development server




