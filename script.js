document.getElementById("symptomForm").addEventListener("submit", function(event) {
  event.preventDefault();

  const input = document.getElementById("symptomInput").value.toLowerCase();
  const symptoms = input.split(",").map(s => s.trim());

  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symptoms: symptoms })
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
