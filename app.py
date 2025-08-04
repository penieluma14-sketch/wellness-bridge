from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
with open("illness_model.pkl", "rb") as f:
    illness_model = pickle.load(f)

@app.route('/diagnose', methods=['POST'])
def diagnose():
    symptoms = request.json['symptoms']  # list/array of encoded symptoms
    
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
    app.run(debug=True)


