import fs from "fs";

const WORDS = [
  "lorem","ipsum","dolor","sit","amet","consectetur","adipiscing","elit",
  "sed","do","eiusmod","tempor","incididunt","ut","labore","et","dolore",
  "magna","aliqua","ut","enim","ad","minim","veniam","quis","nostrud",
  "exercitation","ullamco","laboris","nisi","ut","aliquip","ex","ea",
  "commodo","consequat","duis","aute","irure","dolor","in","reprehenderit"
];

const TARGET_WORDS = 220_000;
let output = [];
for (let i = 0; i < TARGET_WORDS; i++) {
  output.push(WORDS[Math.floor(Math.random() * WORDS.length)]);
}

fs.writeFileSync("corpus.txt", output.join(" "));
console.log("Generated corpus.txt with", TARGET_WORDS, "words");
