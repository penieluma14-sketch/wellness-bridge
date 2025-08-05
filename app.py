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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Convert all symptoms to lowercase and replace spaces with underscores
    input_symptoms = [s.lower().replace(" ", "_") for s in data["symptoms"]]

    # Create the feature vector in the correct order
    input_features = [1 if feature in input_symptoms else 0 for feature in features]

    # Make prediction
    prediction = model.predict([input_features])[0]

    return jsonify({"diagnosis": prediction})

if __name__ == "__main__":
    app.run(debug=True)





