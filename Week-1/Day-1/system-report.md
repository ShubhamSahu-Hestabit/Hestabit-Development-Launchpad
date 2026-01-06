# SHubham Sahu
# DAY 1 — SYSTEM REVERSE ENGINEERING + NODE & TERMINAL MASTERING

## 📁 Project Folder Structure

```text
DAY1-System-Report/
├── system_report.md
├── introspect.js
├── streamBenchmark.js
├── bufferBenchmark.js
├── logs/
│   └── day1-perf.json
└── images/
    ├── OS_version.png
    ├── Current_Shell.png
    ├── which_node.png
    ├── npm_path.png
    ├── all_path.png
    ├── nvm_install.png
    ├── npm_install.png
    ├── node_install.png
    ├── lts_front_back.png
    ├── output_introspectjs.png
    └── json_outcome.png
```

---

## 🔹 Task 1: System Identification

### 1. OS Version

**Command:**

```bash
lsb_release -a
```

**Output:**
![OS Version](Images/OS_version.png)

---

### 2. Current Shell

**Command:**

```bash
echo $SHELL
```

**Output:**
![Current Shell](images/Current_Shell.png)

---

### 3. Node Binary Path



**Command:**

```bash
which node
```

**Output:**
![Which Node](images/which_node.png)

---

### 4. NPM Global Installation Path

**Command:**

```bash
npm root -g
```

**Output:**
![NPM Path](images/npm_path.png)

---

### 5. PATH Entries Containing Node or NPM

**Command:**

```bash
echo $PATH | tr ':' '
' | grep -Ei 'node|npm'
```

**Output:**
![PATH Entries](images/all_path.png)

---

### 2. Current Shell

**Command:**

```bash
echo $SHELL
```

**Output:**
![Current Shell](images/Current_Shell.png)

---

### 3. Node Binary Path

**Command:**

```bash
which node
```

**Output:**
![Which Node](images/which_node.png)

---

### 4. NPM Global Installation Path

**Command:**

```bash
npm root -g
```

**Output:**
![NPM Path](images/npm_path.png)

---

### 5. PATH Entries Containing Node or NPM

**Command:**

```bash
echo $PATH | tr ':' '\n' | grep -Ei 'node|npm'
```

**Output:**
![All PATH Entries](images/all_path.png)

---

## 🔹 Task 2: NVM (Node Version Manager)

### 1. Install NVM

**Command:**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Reload shell:

```bash
source ~/.bashrc
```

**Output:**
![NVM Install](images/nvm_install.png)

---

### 2. Switch Node Versions (LTS ↔ Latest)

Install LTS:

```bash
nvm install --lts
```

Install Latest:

```bash
nvm install node
```

Switch Versions:

```bash
nvm use --lts
nvm use node
```

**Output:**
![LTS ↔ Latest Switch](images/lts_front_back.png)

![Node Install](images/node_install.png)

---

### 2. Switch Node Versions (LTS ↔ Latest)

Install LTS:

```bash
nvm install --lts
```

Install Latest:

```bash
nvm install node
```

Switch Versions:

```bash
nvm use --lts
nvm use node
```

**Output:**
![Node Install](images/node_install.png)

---

## 🔹 Task 3: System Introspection Script

### introspect.js

```js
const os = require('os');
const { execSync } = require('child_process');

console.log('OS:', os.platform());
console.log('Architecture:', os.arch());
console.log('CPU Cores:', os.cpus().length);
console.log('Total Memory (GB):', (os.totalmem() / 1e9).toFixed(2));
console.log('System Uptime (hrs):', (os.uptime() / 3600).toFixed(2));
console.log('Current User:', os.userInfo().username);
console.log('Node Path:', execSync('which node').toString().trim());
```

Run:

```bash
node introspect.js
```

**Output:**
![Introspect Output](images/output_introspectjs.png)

---

## 🔹 Task 4: STREAM vs BUFFER Benchmark

### 1. Create Large Test File (50MB)

```bash
dd if=/dev/urandom of=bigfile.dat bs=1M count=50
```

---

### 2. Buffer Method (fs.readFile)

```js
console.time('Buffer Read');
require('fs').readFile('bigfile.dat', () => {
  console.timeEnd('Buffer Read');
});
```

---

### 3. Stream Method (fs.createReadStream)

```js
console.time('Stream Read');
const fs = require('fs');
const stream = fs.createReadStream('bigfile.dat');
stream.on('end', () => console.timeEnd('Stream Read'));
```

---

### 4. Performance Comparison

| Method | Execution Time | Memory Usage           |
| ------ | -------------- | ---------------------- |
| Buffer | Higher         | High (loads full file) |
| Stream | Lower          | Low (chunk-based)      |

**Observation:** Streams are more memory efficient and scale better for large files.

---

