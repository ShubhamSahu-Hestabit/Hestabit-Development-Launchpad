const http = require("http");
const url = require("url");
const crypto = require("crypto");

const PORT = 3000;

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  // ---------------------------
  // /echo → return headers
  // ---------------------------
  if (pathname === "/echo") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(req.headers, null, 2));
    return;
  }

  // ---------------------------
  // /slow?ms=3000 → delayed response
  // ---------------------------
  if (pathname === "/slow") {
    const delay = parseInt(parsedUrl.query.ms) || 1000;

    setTimeout(() => {
      res.writeHead(200, { "Content-Type": "text/plain" });
      res.end(`Response delayed by ${delay} ms`);
    }, delay);
    return;
  }

  // ---------------------------
  // /cache → cache headers + ETag
  // ---------------------------
  if (pathname === "/cache") {
    const body = JSON.stringify({ message: "Cached response" });
    const etag = crypto.createHash("md5").update(body).digest("hex");

    // If client already has this version
    if (req.headers["if-none-match"] === etag) {
      res.writeHead(304);
      res.end();
      return;
    }

    res.writeHead(200, {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=60",
      "ETag": etag,
    });

    res.end(body);
    return;
  }

  // ---------------------------
  // Default route
  // ---------------------------
  res.writeHead(404, { "Content-Type": "text/plain" });
  res.end("Not Found");
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
