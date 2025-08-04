// Automatically use the same origin for API calls
const apiBaseUrl = `${window.location.origin}/predict`;

document.getElementById("symptomForm").addEventListener("submit", function(event) {
  event.preventDefault();
  
  const input = document.getElementById("symptomInput").value.toLowerCase();
  const symptoms = input.split(",").map(s => s.trim());

  fetch(apiBaseUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ symptoms: symptoms })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById("diagnosisOutput").innerText = data.diagnosis;
  })
  .catch(error => {
    console.error("Error:", error);
    document.getElementById("diagnosisOutput").innerText = "An error occurred while processing your request.";
  });
});
