const fs = require('fs');
const { performance } = require('perf_hooks');  // Import performance from the 'perf_hooks' module
const { memoryUsage } = require('process');

// Function to record performance and memory usage and save it to JSON
const recordPerformance = (label, startTime, startMemory) => {
  const endTime = performance.now();
  const endMemory = memoryUsage().heapUsed;

  const performanceData = {
    label: label,
    executionTimeMs: (endTime - startTime).toFixed(2),  // Execution time in ms
    memoryUsageMB: ((endMemory - startMemory) / (1024 * 1024)).toFixed(2),  // Memory usage in MB
  };

  const filePath = 'day1-perf.json';
  let existingData = [];

  // Check if the JSON file already exists and read the existing data
  if (fs.existsSync(filePath)) {
    try {
      existingData = JSON.parse(fs.readFileSync(filePath));
    } catch (err) {
      console.error("Error reading JSON file:", err);
    }
  }

  existingData.push(performanceData);  // Add the new data to the existing data

  // Write the performance data back to the JSON file
  try {
    fs.writeFileSync(filePath, JSON.stringify(existingData, null, 2));  // Save formatted JSON
    console.log('Performance data saved successfully');
  } catch (err) {
    console.error("Error writing to file:", err);
  }
};

// Start capturing the start time and memory usage
const startTimeBuffer = performance.now();
const startMemoryBuffer = memoryUsage().heapUsed;

// Read the large test file using fs.readFile (Buffer)
fs.readFile('testFile.txt', (err, data) => {
  if (err) {
    console.error("Error reading the file:", err);
    return;
  }

  console.log("File read successfully!");
  // Record the performance data after reading the file
  recordPerformance("Buffer Read (fs.readFile)", startTimeBuffer, startMemoryBuffer);
});
