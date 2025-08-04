from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
with open("illness_model.pkl", "rb") as f:
    illness_model = pickle.load(f)

# Root route so Render home page works
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Medical Diagnosis API is running. Send a POST request to /diagnose with symptom data."
    })

# Diagnose route
@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({"error": "Please provide 'symptoms' in JSON body"}), 400
    
    symptoms = data['symptoms']  # list/array of encoded symptoms
    
    # Predict probabilities
    probabilities = illness_model.predict_proba([symptoms])[0]
    
    # Get illness labels
    illnesses = illness_model.classes_
    
    # Sort by probability (highest first)
    results = sorted(
        zip(illnesses, probabilities),
        key=lambda x: x[1],
        reverse=True
    )
    
    return jsonify({illness: round(prob, 2) for illness, prob in results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



