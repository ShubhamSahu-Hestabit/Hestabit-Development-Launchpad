# NEXUS AI

A production-ready autonomous multi-agent orchestration system that coordinates specialized AI agents with persistent memory capabilities.

---

## Features

- **8 Specialized Agents** — Planner, Researcher, Analyst, Coder, Critic, Optimizer, Validator, Reporter
- **Intelligent Planning** — Auto-decomposes complex tasks into 5-15 executable steps
- **Persistent Memory** — Remembers past conversations and learned facts across sessions
- **Context-Aware** — Uses FAISS semantic search to retrieve relevant past information
- **Failure Recovery** — Each agent step is isolated; errors are logged and execution continues
- **Token-Optimized** — Prevents API overflow with automatic content truncation
- **Logging** — Every run saved to `logs/output_TIMESTAMP.md` and `logs/nexus.log`

---

## Project Structure

```
nexus_ai/
├── agents/
│   ├── orchestrator.py       # Agent coordination + failure recovery
│   ├── planner_agent.py      # Task decomposition
│   ├── researcher_agent.py   # Information gathering
│   ├── analyst_agent.py      # Data analysis
│   ├── coder_agent.py        # Code generation
│   ├── critic_agent.py       # Quality review
│   ├── optimiser_agent.py    # Performance optimization
│   ├── validator_agent.py    # Result validation
│   └── reporter_agent.py     # Report compilation
├── memory/
│   ├── agent_memory.py       # Unified memory system
│   ├── long_term.py          # SQLite persistence
│   ├── vector_memory.py      # FAISS semantic search
│   └── session_memory.py     # Short-term memory
├── vectorstore/              # Auto-created on first run
│   ├── agent_long_term.db
│   ├── agent_vectors.faiss
│   └── agent_vectors.faiss.meta
├── logs/                     # Auto-created on first run
│   ├── nexus.log
│   └── output_TIMESTAMP.md
├── config.py                 # Model client + logging setup
├── main.py                   # Entry point
├── .env                      # API key
├── README.md
├── ARCHITECTURE.md
└── FINAL-REPORT.md
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install autogen-agentchat autogen-ext[openai] faiss-cpu sentence-transformers python-dotenv

# 2. Add your Groq API key (free at console.groq.com)
echo "GROQ_API_KEY=gsk_..." > .env

# 3. Run
python main.py
```

---

## Example Tasks

```
Task: Design a RAG pipeline for 10k documents
Task: Plan a startup in AI for healthcare
Task: Generate backend architecture for a scalable app
Task: Analyze CSV and create a business strategy
Task: What did we discuss last time?
```

---

## Commands

| Input | Action |
|-------|--------|
| Any task | Full multi-agent execution |
| `stats` | Show memory statistics |
| `quit` | Save and exit |

---

## Memory Layers

| Layer | Storage | Persists? | Purpose |
|-------|---------|-----------|---------|
| Session | RAM | No | Recent conversation context |
| Vector | FAISS | Yes | Semantic similarity search |
| Long-term | SQLite | Yes | Important facts and results |

---

## How It Works

```
User: "Design a RAG pipeline for 10k documents"
  ↓
Memory retrieves: "Shubham is an AI engineer at Hestabit"
                  "Previously discussed vector store options"
  ↓
Planner creates: 9-step execution plan
  [Researcher → Analyst → Coder → Critic → Optimizer → Validator → Reporter]
  ↓
Each agent executes with full context from previous steps
  ↓
Reporter compiles final production-ready document
  ↓
Result saved to memory for next session
```

---

## Documentation

- **README.md** — Quick start and usage
- **ARCHITECTURE.md** — Detailed system architecture
- **FINAL-REPORT.md** — Complete project report
