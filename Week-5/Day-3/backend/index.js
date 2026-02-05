import express from "express";
import os from "os";

const app = express();

app.get("/api", (req, res) => {
  res.json({
    message: "Handled by backend",
    container: os.hostname()
  });
});

app.listen(3000, () => {
  console.log("Backend running on port 3000");
});
