# Final Project Report — NEXUS AI

---

## Executive Summary

Built an autonomous multi-agent orchestration system that intelligently decomposes complex tasks, executes them using 7 specialized AI agents, and maintains persistent memory across sessions using a 3-tier hybrid memory architecture.

---

## Objectives

1. Create an orchestrator that coordinates multiple specialized agents
2. Implement intelligent task decomposition and dynamic planning
3. Build a persistent memory system with semantic search
4. Optimize for token efficiency to prevent API errors
5. Add failure recovery so one agent error does not crash the pipeline

---

## Technical Implementation

### Core Components

#### 1. Orchestrator — `agents/orchestrator.py`
- Central coordinator for multi-agent workflows
- Memory context injection before planning
- Sequential task execution with context passing
- Per-step failure recovery — errors logged, execution continues
- Content truncation to prevent token overflow

#### 2. Agent System

8 agents total: 1 planner + 7 execution agents. Each wraps AutoGen's `AssistantAgent`.

| Agent | Responsibility |
|-------|---------------|
| Planner | Decomposes task into JSON execution plan |
| Researcher | Information gathering and best practices |
| Analyst | Trade-off analysis, risk evaluation |
| Coder | Clean, commented code generation |
| Critic | Quality review, issue identification |
| Optimizer | Performance and cost optimization |
| Validator | Correctness and completeness checks |
| Reporter | Final report compilation |

#### 3. Memory System — `memory/agent_memory.py`

Three-layer memory hierarchy:

| Layer | Backend | Capacity | Persistence |
|-------|---------|----------|-------------|
| Session | RAM list | 50 turns | No |
| Vector | FAISS (384-dim) | Unlimited | Yes |
| Long-term | SQLite | Unlimited | Yes |

**Importance scoring** (0-10):
- `importance=9` — critical user facts (e.g. "Shubham is an AI engineer at Hestabit")
- `importance=7` — completed task results
- `importance=6` — agent outputs and user goals
- `importance=5` — general context

---

## Example Workflows

### Workflow 1: Memory-Aware Task Execution

```
Session 1:
You: My name is Shubham and I work at Hestabit as an AI engineer
Agent: Nice to meet you Shubham! Saved to memory.

You: I love building multi-agent AI systems
Agent: Saved: 1 user fact, 1 context fact
       [USER] Interested in building multi-agent AI systems → SQLite (importance=9)

You: quit → FAISS + SQLite saved to disk

Session 2 (restart):
Loaded: 1 facts, 1 embeddings

You: Design a RAG pipeline for 10k documents
  ↓
Memory retrieved:
  • "Shubham is an AI engineer at Hestabit" (importance=9)
  • "Interested in building multi-agent AI systems" (similarity=0.65)
  ↓
Planner creates 9-step plan with Shubham's background as context
  ↓
Agents execute with full awareness of user's expertise level
```

### Workflow 2: RAG Pipeline Design

```
Task: "Design a RAG pipeline for 10k documents"
  ↓
Memory: Retrieves Shubham's AI engineering background
  ↓
Planner: Creates 9-step plan
  [Researcher → Analyst → Analyst → Coder → Coder →
   Critic → Optimizer → Validator → Reporter]
  ↓
Researcher: Vector store options (FAISS, Milvus, Pinecone),
            embedding models, chunking strategies
Analyst:    Requirements analysis, trade-offs, latency targets
Coder:      Ingestion script, retrieval module, prompt construction
Critic:     Security review, error handling gaps
Optimizer:  Redis caching, batching, async processing
Validator:  End-to-end test scenarios, accuracy metrics
Reporter:   Production-ready document with architecture + code
  ↓
Output saved to logs/output_TIMESTAMP.md
Memory: 9 entries saved (importance 6-7)
```

### Workflow 3: Healthcare Startup Planning

```
Task: "Plan a startup in AI for healthcare"
  ↓
Memory: "Shubham is AI engineer at Hestabit" context injected
  ↓
Planner: Creates 10-step plan
  ↓
Output: Market analysis, MVP features, financial model, risk assessment
Memory: 10+ entries saved
```

---

## Key Achievements

### 1. Intelligent Task Decomposition
- Planner automatically breaks complex tasks into 5-15 ordered steps
- JSON execution plans with specific agent assignments
- Memory-aware planning — user background injected into every plan

### 2. Persistent Memory
- Survives system restarts (FAISS + SQLite)
- Importance-based retrieval (threshold >= 7)
- Semantic similarity search (threshold >= 0.3)
- Deduplication across memory layers

### 3. Failure Recovery
- Each agent step wrapped in try/except
- Errors logged to `logs/nexus.log` with full traceback
- Pipeline continues even if one agent fails
- Failed steps recorded in results with ERROR prefix

### 4. Token Efficiency
- Using `llama-3.3-70b-versatile` with 131k context window
- Content truncation at 500/400/250/200/150 char limits per context section
- Zero token overflow errors in production

### 5. Logging
- Every run → `logs/output_TIMESTAMP.md`
- Full debug trace → `logs/nexus.log`
- TeeOutput writes to terminal and file simultaneously

---

## Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Token overflow | Content truncation + 131k context model |
| Silent crashes | `traceback.print_exc()` + per-step try/except |
| Memory duplication | Deduplication by content in retrieval |
| Hardcoded task | Replaced with interactive CLI loop |
| No logging | TeeOutput + file handler in config.py |
| Model too small | Upgraded from 8b to 70b for complex tasks |

---

## Performance

| Metric | Result |
|--------|--------|
| Speed | 30-120s per workflow |
| Steps per task | 5-15 |
| Token overflow errors | 0 |
| Memory persistence | FAISS + SQLite survive restart |
| Storage | < 1MB typical |

---

## File Structure

```
nexus_ai/
├── agents/
│   ├── orchestrator.py
│   ├── planner_agent.py
│   ├── researcher_agent.py
│   ├── analyst_agent.py
│   ├── coder_agent.py
│   ├── critic_agent.py
│   ├── optimiser_agent.py
│   ├── validator_agent.py
│   └── reporter_agent.py
├── memory/
│   ├── agent_memory.py
│   ├── long_term.py
│   ├── vector_memory.py
│   └── session_memory.py
├── vectorstore/
│   ├── agent_long_term.db
│   ├── agent_vectors.faiss
│   └── agent_vectors.faiss.meta
├── logs/
│   ├── nexus.log
│   └── output_TIMESTAMP.md
├── config.py
├── main.py
├── .env
├── README.md
├── ARCHITECTURE.md
└── FINAL-REPORT.md
```

---

## Code Statistics

| Component | Files |
|-----------|-------|
| Agents | 9 |
| Memory | 4 |
| Config + Main | 2 |
| Docs | 3 |
| **Total** | **18** |

---




