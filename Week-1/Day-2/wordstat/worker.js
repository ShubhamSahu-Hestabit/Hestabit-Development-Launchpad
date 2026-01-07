import { parentPort, workerData } from "worker_threads";

const { text, minLen } = workerData;

const words = text.toLowerCase().match(/\b[a-z]+\b/g) || [];

const result = {
  total: words.length,
  freq: {},
  longest: "",
  shortest: null
};

for (const word of words) {
  if (word.length < minLen) continue;

  result.freq[word] = (result.freq[word] || 0) + 1;

  if (word.length > result.longest.length) result.longest = word;
  if (!result.shortest || word.length < result.shortest.length) {
    result.shortest = word;
  }
}

parentPort.postMessage(result);

