const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
const PORT = 8080;

app.use(cors());

app.use(express.json());

// POST 

app.post("/analyze", async (req, res) => {
  try {

    const message = req.body.message;

    if (!message) {
      return res.status(400).json({
        error: "Message is required"
      });
    }

    const aiResponse = await axios.post(
      "http://localhost:8000/analyze",
      { message: message }
    );

    return res.json(aiResponse.data);

  } catch (error) {
    console.error("Backend error:", error.message);

    return res.status(500).json({
      error: "AI service is not available"
    });
  }
});


app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});