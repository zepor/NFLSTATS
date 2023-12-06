const express = require("express");
const path = require("path");
const app = express();

// Serve static files from the 'dist' directory
app.use(express.static(path.join(__dirname, "dist")));

// Special handling for ACME challenge route
app.get("/.well-known/acme-challenge/*", (req, res) => {
  res.sendFile(path.join(__dirname, "dist", "index.html"));
});

// Handle all other routes
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "dist", "index.html"));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
