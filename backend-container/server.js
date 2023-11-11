const express = require('express');
const app = express();
const port = process.env.PORT || 5000;
const path = require('path');
// Serve static files from the React app
app.use(express.static(path.join(__dirname, '../frontend/build')));
// The "catchall" handler: for any request that doesn't match one above, send back React's index.html file.
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
});
app.get('/api', (req, res) => {
    res.send({ message: 'Hello from Express!' });
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
