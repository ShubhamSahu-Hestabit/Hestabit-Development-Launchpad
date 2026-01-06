const fs = require('fs');

// Create a large file with 50MB of random data
const data = Buffer.alloc(50 * 1024 * 1024);  // 50MB buffer filled with zeroes

fs.writeFileSync('testFile.txt', data);
console.log('50MB file created successfully');
