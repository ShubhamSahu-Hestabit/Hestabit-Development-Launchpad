# Week 1 — Engineering Mindset Bootcamp (Learning & Reflection)

---

## Repository Structure

```
Week-1/
├── Day-1/
├── Day-2/
├── Day-3/
├── Day-4/
├── Day-5/
   └── WEEK1-RETRO.md
```
---

## Environment & Tools

- OS: Linux (Ubuntu)
- Shell: bash
- Node.js (via NVM)
- Git & GitHub
- curl & Postman
- ESLint, Prettier, Husky
- cron

Most of the work was done **entirely using the terminal**, without relying on GUI tools.

---

## Day 1 — System Reverse Engineering & Node Internals

### What I Worked On
- Inspected OS, shell, PATH, and Node binary resolution.
- Installed and switched Node versions using NVM.
- Created `introspect.js` to fetch system-level information.
- Benchmarked **Buffer vs Stream** file reading for large files.

### Useful Commands
```bash
uname -a
echo $SHELL
echo $PATH
which node
node -v
nvm ls
```

### Key Learning
- PATH controls which Node version runs.
- Streams are safer for large files.
- Performance must be measured, not assumed.

![Day 1 Screenshot](Day-5/images/day1.png)

---

## Day 2 — Node CLI Tool & Large Data Processing

### What I Built
- Generated a corpus file with 200,000+ words.
- Built `wordstat.js`, a CLI tool for text analysis.
- Implemented concurrency using chunk-based processing.
- Benchmarked performance at multiple concurrency levels.

### Example Command
```bash
node wordstat.js --file corpus.txt --top 10 --minLen 5 --unique
```

### Key Learning
- Correctness comes before concurrency.
- CLI design matters for usability.
- Benchmarks reveal real system limits.

![Day 2 Screenshot](Day-5/images/day2.png)

---

## Day 3 — Git Mastery (Merge, Rebase & Recovery)

### What I Practiced
- Created multiple commits and intentionally introduced a bug.
- Used `git bisect` to find the faulty commit.
- Fixed the issue using `git revert`.
- Practiced stash workflow.
- Resolved real merge conflicts using two local clones.

### What Actually Broke
- Merge conflicts took time to understand.
- Confusion between **merge vs rebase**.
- Pull failures due to unstaged changes during rebase attempts.

### Useful Commands
```bash
git status
git pull
git pull --rebase
git bisect
git revert <commit>
git stash
```

### Key Learning
- Rebase rewrites history and should be avoided on shared branches.
- Merge preserves context and is safer.
- Git is a recovery tool, not just version control.

![Day 3 Screenshot](Day-5/images/day3.png)

---

## Day 4 — HTTP / API Forensics & Git File Issues

### What I Investigated
- DNS lookup and traceroute.
- HTTP request/response inspection using curl.
- Pagination and caching using ETag.
- Built a small Node HTTP server for testing.

### Git Issue Faced
- Uploaded images via GitHub UI initially.
- Later moved the same images locally.
- Git showed confusing file states due to duplicated tracking.

### Useful Commands
```bash
curl -v https://dummyjson.com/products?limit=5
git status
git rm <file>
```

### Key Learning
- Mixing GitHub UI and local Git workflows causes issues.
- Repository structure should be decided early.

![Day 4 Screenshot](Day-5/images/day4.png)

---

## Day 5 — Automation & Mini CI Pipeline

### What I Automated
- Created `validate.sh` to verify structure and config.
- Added ESLint and Prettier.
- Configured Husky pre-commit hooks.
- Created build artifacts with checksum.
- Scheduled scripts using cron.

### Structural Mistake
- Created a folder outside the main repo by mistake.
- This broke hooks and scripts.
- Fixed by restructuring and reinitializing setup.

### Useful Commands
```bash
bash validate.sh
npm run lint
crontab -e
```

### Key Learning
- Automation fails silently if paths are wrong.
- Structure is as important as code.

![Day 5 Screenshot](Day-5/images/day5.png)

---

## Personal Reflection

- Most learning came from debugging real issues.
- Git became clearer only after real conflicts.
- I am moving from heavy AI usage to **documentation-first learning**.
- Writing explanations improved my understanding significantly.

---
## Mistakes That Helped Me Learn

- Misusing `git rebase` during merge conflicts
- Mixing GitHub UI uploads with local Git workflow
- Creating incorrect folder structures inside the repository
- Assuming things without verifying through logs or commands

---

## How My Learning Approach Changed

- Earlier, I relied heavily on AI tools for solutions.
- This week, I consciously shifted towards:
  - Reading official documentation
  - Testing things manually in the terminal
  - Writing my own explanations and notes


---


**Author:** Shubham Sahu  
**Role:** Trainee Software Engineer  
**Program:** Hestabit Development Launchpad
