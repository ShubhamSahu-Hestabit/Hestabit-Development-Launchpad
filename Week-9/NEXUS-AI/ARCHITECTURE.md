# NEXUS AI - System Architecture

## Overview

Autonomous multi-agent orchestration system with persistent memory, built on AutoGen framework and Groq LLM infrastructure.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│                          (main.py)                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR LAYER                        │
│              (MemoryEnabledOrchestrator)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Memory Context Builder                              │   │
│  │  - Retrieves important facts (importance >= 7)       │   │
│  │  - Queries vector store (top-k semantic search)      │   │
│  │  - Fetches recent session (last 2 turns)             │   │
│  │  - Truncates content to prevent token overflow       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      PLANNING LAYER                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  PlannerAgent                                        │   │
│  │  - Decomposes task into ordered steps                │   │
│  │  - Assigns steps to specialized agents               │   │
│  │  - Outputs strict JSON execution plan                │   │
│  │  - Considers full memory context                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION LAYER                           │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │Researcher│ Analyst  │  Coder   │  Critic  │Optimizer │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
│  ┌──────────┬──────────┐                                     │
│  │Validator │ Reporter │                                     │
│  └──────────┴──────────┘                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      MEMORY LAYER                            │
│                   (AgentMemorySystem)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Session Memory (RAM)                                │   │
│  │  - Last 50 conversation turns                        │   │
│  │  - Temporary context window                          │   │
│  │  - Cleared on restart                                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Vector Store (FAISS)                                │   │
│  │  - Semantic embeddings via all-MiniLM-L6-v2          │   │
│  │  - Similarity search (cosine via L2 normalized)      │   │
│  │  - 384-dim vectors, top-k=5, threshold=0.3           │   │
│  │  - Persisted: agent_vectors.faiss + .meta            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Long-term Memory (SQLite)                           │   │
│  │  - Persistent storage with importance scoring        │   │
│  │  - Type classification (semantic/episodic)           │   │
│  │  - Indexed queries on importance and type            │   │
│  │  - File: agent_long_term.db                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Orchestrator

**File**: `agents/orchestrator.py`
**Class**: `MemoryEnabledOrchestrator`

**Responsibilities**:
- Coordinate workflow execution across multiple agents
- Build comprehensive memory context before planning
- Manage agent communication and result aggregation
- Save execution results to persistent memory
- Handle failure recovery per step — errors are logged, execution continues

**Key Methods**:
```python
execute(user_goal)
_build_memory_context(query)
_build_agent_context(task, previous_results, ...)
_save_to_memory(content, importance, memory_type)
_truncate(content, max_length)
_parse_plan(plan_response)
_compile_results(results)
```

---

### 2. Planner Agent

**File**: `agents/planner_agent.py`
**Purpose**: Task decomposition and agent assignment

**Input**: User goal + Memory context
**Output**: JSON execution plan

```json
{
  "steps": [
    {"agent": "Researcher", "task": "Research healthcare AI market trends 2026"},
    {"agent": "Analyst",    "task": "Analyze competitor landscape and market gaps"},
    {"agent": "Coder",      "task": "Design MVP feature set and system architecture"},
    {"agent": "Critic",     "task": "Review feasibility and compliance requirements"},
    {"agent": "Reporter",   "task": "Compile final startup plan document"}
  ]
}
```

---

### 3. Execution Agents

| Agent | Role | Output |
|-------|------|--------|
| **Researcher** | Information gathering | Research findings, best practices |
| **Analyst** | Trade-off evaluation | Insights, patterns, risk assessment |
| **Coder** | Code generation | Clean, commented, working code |
| **Critic** | Quality review | Problems, flaws, improvement suggestions |
| **Optimizer** | Performance tuning | Optimizations, efficiency improvements |
| **Validator** | Correctness verification | Validation report, pass/fail status |
| **Reporter** | Result compilation | Structured final report |

---

### 4. Memory System

**File**: `memory/agent_memory.py`
**Class**: `AgentMemorySystem`

#### Session Memory
- Storage: In-memory list
- Capacity: 50 turns
- Persistence: No (clears on restart)
- File: `memory/session_memory.py`

#### Vector Store
- Backend: FAISS (IndexFlatL2)
- Model: all-MiniLM-L6-v2 (384-dim)
- Similarity: Cosine (L2 normalized)
- Config: k=5, threshold=0.3
- Persistence: Yes → `vectorstore/agent_vectors.faiss`
- File: `memory/vector_memory.py`

#### Long-term Memory
- Backend: SQLite
- Persistence: Yes → `vectorstore/agent_long_term.db`
- File: `memory/long_term.py`

**Schema**:
```sql
CREATE TABLE memories (
    id          INTEGER PRIMARY KEY,
    content     TEXT,
    memory_type TEXT,       -- 'semantic' or 'episodic'
    mime_type   TEXT,
    metadata    TEXT,
    importance  INTEGER,    -- 0-10 score
    created_at  TIMESTAMP
);
CREATE INDEX idx_memory_type ON memories(memory_type);
CREATE INDEX idx_importance  ON memories(importance DESC);
```

---

## Memory Context Format

Agents receive context in structured sections:

```
=== IMPORTANT CONTEXT ===
 • Shubham is an AI engineer at Hestabit
 • Interested in building multi-agent AI systems

=== RELEVANT PAST ===
 • Previously discussed RAG pipeline design
 • Built scalable backend architecture last session

=== RECENT ===
 • User: Design a RAG pipeline for 10k documents
 • System created 9-step execution plan

=== ORIGINAL GOAL ===
Design a RAG pipeline for 10k documents

=== YOUR TASK ===
Research vector store options (FAISS, Milvus, Pinecone) and embedding
models suitable for 10k document RAG pipeline

=== PREVIOUS STEP ===
 • Researcher: Collected best practices on chunking strategies...
```

---

## Data Flow

### Task Execution Flow

```
1. User Input
   ↓
2. Orchestrator receives task
   ↓
3. Query memory for relevant context
   - Long-term: get_important_memories(importance >= 7, limit=3)
   - Vector:    query(user_goal, k=2)
   - Session:   get_recent(n=2)
   ↓
4. Build memory context (formatted sections with truncation)
   ↓
5. Planner creates JSON execution plan
   ↓
6. Save user goal to memory (importance=6, episodic)
   ↓
7. For each step:
   a. Build agent context (memory + task + previous)
   b. Execute agent
   c. If error → log and continue (failure recovery)
   d. Save result to memory (importance=6, episodic)
   ↓
8. Compile final result (Reporter output preferred)
   ↓
9. Save to long-term (importance=7, semantic)
   ↓
10. Return to user + save to logs/output_TIMESTAMP.md
```

### Memory Save Flow

```
Content
  ↓
Truncate to 500 chars
  ↓
MemoryContent(content, mime_type, metadata)
  ↓
AgentMemorySystem.add(store_long_term=True)
  ↓
┌────────────────┬────────────────┬────────────────┐
│  Session.add() │  Vector.add()  │ LongTerm.add() │
│  (RAM list)    │  (FAISS index) │  (SQLite DB)   │
└────────────────┴────────────────┴────────────────┘
```

---

## Logging

All runs logged to:
- `logs/nexus.log` — full DEBUG trace (persistent)
- `logs/output_TIMESTAMP.md` — per-run output file

---

## Config

**File**: `config.py`

| Priority | Model | Condition |
|----------|-------|-----------|
| 1st | Groq `llama-3.3-70b-versatile` | `GROQ_API_KEY` set in `.env` |
| 2nd | Ollama `qwen2.5:7b-instruct-q4_0` | Fallback if no key |
