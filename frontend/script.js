function enterApp() {
  const login = document.getElementById("loginPage");
  const app = document.getElementById("appPage");

  login.style.display = "none";
  app.style.display = "block";
  console.log("Login:", login);
console.log("App:", app);

}

function scrollToAnalyzer() {
  document.getElementById("analyzer").scrollIntoView({
    behavior: "smooth"
  });
}

//text
function resetText() {
  document.getElementById("message").value = "";
  document.getElementById("analysisReport").innerHTML = "Awaiting analysis...";
  updateRisk(0, "textCircle", "textRiskNumber", "textRiskStatus");
}

//risk
function updateRisk(score, circleId, numberId, statusId) {
  const circle = document.getElementById(circleId);
  const number = document.getElementById(numberId);
  const status = document.getElementById(statusId);

  const radius = 85;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  circle.style.strokeDasharray = circumference;
  circle.style.strokeDashoffset = offset;

  number.innerText = score + "%";

  if (score <= 30) {
    circle.style.stroke = "#22c55e";
    status.className = "risk-status safe";
    status.innerText = "SAFE";
  }
  else if (score <= 70) {
    circle.style.stroke = "#facc15";
    status.className = "risk-status medium";
    status.innerText = "MEDIUM";
  }
  else {
    circle.style.stroke = "#ef4444";
    status.className = "risk-status high";
    status.innerText = "HIGH RISK";
  }
}

async function checkMessage() {

  const message = document.getElementById("message").value;
  const reportBox = document.getElementById("analysisReport");

  if (!message.trim()) return;

  reportBox.innerHTML = "Analyzing with AI security engine...";

  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    // Update risk circle
    const score = Math.round(data.risk_score || 0);
    updateRisk(score, "textCircle", "textRiskNumber", "textRiskStatus");

    // Explanation
    let reasonsHTML = "";

    if (data.reasons && data.reasons.length > 0) {
      reasonsHTML += "<strong>Why this message is risky:</strong><ul>";
      data.reasons.forEach(r => {
        reasonsHTML += `<li>${r}</li>`;
      });
      reasonsHTML += "</ul>";
    } else {
      reasonsHTML += "<strong>No strong threat indicators detected.</strong>";
    }

    // Module breakdown
    let moduleHTML = "<br><strong>Security Modules Triggered:</strong><ul>";

    for (const module in data.module_findings) {
      if (data.module_findings[module].length > 0) {
        moduleHTML += `<li>${module.replace("_"," ")} detected suspicious behavior</li>`;
      }
    }

    moduleHTML += "</ul>";

    reportBox.innerHTML = reasonsHTML + moduleHTML;

  } catch (error) {
    reportBox.innerHTML = "Unable to contact AI backend.";
  }
}

async function scanAttachment() {

  const fileInput = document.getElementById("fileInput");

  if (!fileInput.files.length) {
    alert("Please choose a PDF first.");
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  try {

    const response = await fetch("http://127.0.0.1:8000/scan_attachment", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    // Calculate risk score
    let score = 0;

    if (data.risk) {
      score = 85; // suspicious attachment
    } else {
      score = 10; // mostly safe
    }

    // Update the PDF risk meter
    updateRisk(score, "imageCircle", "imageRiskNumber", "imageRiskStatus");

  } catch (error) {
    alert("Attachment scanner failed. Backend may not be running.");
  }
}

async function scanURL() {

  const url = document.getElementById("urlInput").value;
  const reportBox = document.getElementById("urlReport");

  if (!url.trim()) {
    reportBox.innerHTML = "Please enter a URL first.";
    return;
  }

  reportBox.innerHTML = "Analyzing URL infrastructure...";

  try {

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: url })
    });

    const data = await response.json();

    // update risk meter
    const score = Math.round(data.risk_score || 0);
    updateRisk(score, "urlCircle", "urlRiskNumber", "urlRiskStatus");

    // explanation
    let explanation = "";

    if (data.reasons && data.reasons.length > 0) {
      explanation += "<strong>Detected Issues:</strong><ul>";
      data.reasons.forEach(r => {
        explanation += `<li>${r}</li>`;
      });
      explanation += "</ul>";
    } else {
      explanation = "No obvious phishing indicators found.";
    }

    reportBox.innerHTML = explanation;

  } catch (error) {
    reportBox.innerHTML = "Unable to connect to AI backend.";
  }
}

document.getElementById("fileInput").addEventListener("change", function() {
  const fileName = this.files[0]?.name;
  if (fileName) {
    document.getElementById("fileNameDisplay").innerText = "Selected: " + fileName;
  }
});