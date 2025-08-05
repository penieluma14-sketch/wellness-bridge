document.getElementById("symptomForm").addEventListener("submit", function(event) {
  event.preventDefault();

  const input = document.getElementById("symptomInput").value.toLowerCase();
  
  // Split input by commas and trim spaces
  const symptoms = input.split(",").map(s => s.trim());

  // The 10 features in the same order as the backend expects
  const allFeatures = [
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
  ];

  // Create final list only with valid features
  const matchedSymptoms = symptoms.filter(symptom => allFeatures.includes(symptom));

  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symptoms: matchedSymptoms })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById("diagnosisOutput").innerText = data.diagnosis;
  })
  .catch(error => {
    console.error("Error:", error);
    document.getElementById("diagnosisOutput").innerText = "An error occurred.";
  });
});
