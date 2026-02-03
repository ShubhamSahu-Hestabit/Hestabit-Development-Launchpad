const http = require('http');
const os = require('os');

const PORT = 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`
    <h1>Hello from Docker Container!</h1>
    <p>Hostname: ${os.hostname()}</p>
    <p>Platform: ${os.platform()}</p>
    <p>Time: ${new Date().toISOString()}</p>
  `);
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Container hostname: ${os.hostname()}`);
});
