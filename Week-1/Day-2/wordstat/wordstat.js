#!/usr/bin/env node
import fs from "fs";
import { Worker } from "worker_threads";
import { performance } from "perf_hooks";

const args = process.argv.slice(2);

function getArg(flag, def) {
  const idx = args.indexOf(flag);
  return idx !== -1 ? args[idx + 1] : def;
}

const file = getArg("--file");
const topN = parseInt(getArg("--top", "10"));
const minLen = parseInt(getArg("--minLen", "1"));
const concurrency = parseInt(getArg("--concurrency", "1"));

if (!file) {
  console.error("Usage: wordstat --file <file> [--top N] [--minLen N] [--concurrency N]");
  process.exit(1);
}

const text = fs.readFileSync(file, "utf8");
const chunkSize = Math.ceil(text.length / concurrency);
const chunks = [];

for (let i = 0; i < concurrency; i++) {
  chunks.push(text.slice(i * chunkSize, (i + 1) * chunkSize));
}

function runWorker(chunk) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(new URL("./worker.js", import.meta.url), {
      workerData: { text: chunk, minLen }
    });
    worker.on("message", resolve);
    worker.on("error", reject);
  });
}

(async () => {
  const start = performance.now();
  const results = await Promise.all(chunks.map(runWorker));

  const freq = {};
  let totalWords = 0;
  let longest = "";
  let shortest = null;

  for (const r of results) {
    totalWords += r.total;

    for (const [w, c] of Object.entries(r.freq)) {
      freq[w] = (freq[w] || 0) + c;
    }

    if (r.longest.length > longest.length) longest = r.longest;
    if (!shortest || (r.shortest && r.shortest.length < shortest.length)) {
      shortest = r.shortest;
    }
  }

  const topWords = Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN)
    .map(([word, count]) => ({ word, count }));

  const end = performance.now();
  const runtimeMs = Number((end - start).toFixed(2));

  console.log("\n=== WORD STATS ===");
  console.log("Total words:", totalWords);
  console.log("Unique words:", Object.keys(freq).length);
  console.log("Longest word:", longest);
  console.log("Shortest word:", shortest);
  console.log("Top words:", topWords);

  // ---- OUTPUT FILE ----
  fs.mkdirSync("output", { recursive: true });
  fs.writeFileSync(
    "output/stats.json",
    JSON.stringify(
      {
        totalWords,
        uniqueWords: Object.keys(freq).length,
        longestWord: longest,
        shortestWord: shortest,
        topWords
      },
      null,
      2
    )
  );

  // ---- PERFORMANCE LOG ----
  fs.mkdirSync("logs", { recursive: true });
  const perfFile = "logs/perf-summary.json";

  let perf = [];
  if (fs.existsSync(perfFile)) {
    perf = JSON.parse(fs.readFileSync(perfFile, "utf8"));
  }

  perf.push({
    concurrency,
    runtimeMs,
    timestamp: new Date().toISOString()
  });

  fs.writeFileSync(perfFile, JSON.stringify(perf, null, 2));
})();
