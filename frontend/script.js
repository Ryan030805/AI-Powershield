async function checkMessage() {
  const message = document.getElementById("message").value;

  const response = await fetch("http://localhost:8080/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: message })
  });

  const data = await response.json();

  document.getElementById("result").innerText =
    "Result: " + data.label + 
    " | Confidence: " + data.confidence +
    "\nReason: " + data.reason;
}