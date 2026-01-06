const os = require('os');

console.log("OS:", os.platform(), os.release());
console.log("Architecture:", os.arch());
console.log("CPU Cores:", os.cpus().length);
console.log("Total Memory:", (os.totalmem() / (1024 * 1024 * 1024)).toFixed(2) + " GB");
console.log("System Uptime:", (os.uptime() / 60).toFixed(2) + " minutes");
console.log("Current Logged User:", os.userInfo().username);
console.log("Node Path:", process.argv[0]);
