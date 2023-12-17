const express = require("express");
const path = require("path");
const app = express();

const distPath = path.join(__dirname, "dist");
console.log(`Serving static files from: ${distPath}`);

app.use(express.static(distPath));

app.get("*", function (req, res) {
  const indexPath = path.join(distPath, "index.html");
  console.log(`Attempting to serve: ${indexPath}`);
  res.sendFile(indexPath);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
