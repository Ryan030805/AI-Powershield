const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
const PORT = 8080;

// Allow frontend to talk to backend
app.use(cors());

// Allow backend to read JSON body
app.use(express.json());

// ------------------------------------
// POST /analyze
// ------------------------------------
app.post("/analyze", async (req, res) => {
  try {
    // 1. Read message from frontend
    const message = req.body.message;

    if (!message) {
      return res.status(400).json({
        error: "Message is required"
      });
    }

    // 2. Send message to FastAPI AI
    const aiResponse = await axios.post(
      "http://localhost:8000/analyze",
      { message: message }
    );

    // 3. Return AI response to frontend
    return res.json(aiResponse.data);

  } catch (error) {
    console.error("Backend error:", error.message);

    return res.status(500).json({
      error: "AI service is not available"
    });
  }
});

// Start backend server
app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});