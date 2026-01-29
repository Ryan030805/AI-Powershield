async function checkMessage() {
  const message = document.getElementById("message").value;
  const resultDiv = document.getElementById("result");

  if (!message.trim()) {
    resultDiv.style.display = "block";
    resultDiv.className = "legend-phishing";
    resultDiv.innerText = "Please enter a message to analyze.";
    return;
  }

  resultDiv.style.display = "block";
  resultDiv.className = "";
  resultDiv.innerText = "Analyzing message...";

  try {
    const response = await fetch("http://localhost:8080/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    if (data.label === "Safe") {
      resultDiv.className = "legend-safe";
      resultDiv.innerHTML = `
        <strong>Message Appears Safe</strong><br><br>
        This message does not show strong signs of phishing or malicious intent.
        <div class="legend-text">
          You can proceed normally, but always stay cautious online.
        </div>
      `;
    } else {
      resultDiv.className = "legend-phishing";
      resultDiv.innerHTML = `
        <strong>Potential Phishing Detected</strong><br><br>
        This message shows patterns commonly used in phishing attacks such as
        urgency, fear, or sensitive information requests.
        <div class="legend-text">
          It is recommended NOT to click any links or share personal details.
        </div>
      `;
    }

  } catch (error) {
    resultDiv.className = "legend-phishing";
    resultDiv.innerText = "Error connecting to AI service.";
  }
}