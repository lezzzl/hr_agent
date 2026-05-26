# HR Screening Agent

AI-agent for primary HR screening in an ML team. The project started as a notebook prototype and was refactored into a LangGraph application with a reusable service layer, RAG knowledge base, interview scheduling tools, LangSmith Studio support, and a Telegram interface.

The agent conducts a short structured interview, validates candidate answers, extracts skills, predicts the most suitable ML-team role, answers HR-related questions from a local knowledge base, and can book interview slots in a local SQLite schedule.

## Features

- Multi-step HR interview with stateful dialogue.
- Input guardrail for off-topic messages and prompt-injection attempts.
- Re-ask logic when a candidate answers the wrong question.
- Candidate profile collection across 9 interview questions.
- Skill extraction and role selection for:
  - Project Manager
  - Data Analyst
  - Data Engineer
  - Data Scientist
  - MLOps Engineer
  - Not Suitable
- HyDE-enhanced RAG over local HR documents using Chroma and Hugging Face embeddings.
- Tool-based answers for hiring process, role requirements, work format, compensation, and FAQ.
- SQLite-based interview slot listing and booking.
- LangSmith / LangGraph Studio integration.
- Telegram bot wrapper with `/start`, `/reset`, and `/help`.
- LangSmith datasets for role classification and dialogue policy checks.

## Tech Stack

- Python 3.11+
- LangGraph
- LangChain Core
- OpenRouter chat model
- LangSmith tracing and Studio
- Chroma vector store
- Hugging Face `intfloat/multilingual-e5-small` embeddings
- SQLite
- python-telegram-bot
- python-dotenv

## Architecture

```text
Telegram / CLI / Studio
        |
        v
hr_agent_app.service.handle_message
        |
        v
LangGraph state graph
        |
        +-- input_check_node
        +-- interview_node
        +-- skills_extraction_node
        +-- role_selection_node
        +-- formatter_node
        +-- agent_node
              |
              +-- search_hr_documents tool
              |     |
              |     +-- HyDE query expansion
              |     +-- Chroma vector store
              |     +-- Hugging Face embeddings
              |     +-- data/hr_docs/*.md
              |
              +-- list_interview_slots tool
              +-- book_interview_slot tool
                    |
                    +-- SQLite schedule database
```

## Repository Structure

```text
hr_agent_app/
  cli.py                  # Local CLI interface
  config.py               # Environment and model configuration
  graph.py                # LangGraph graph definition
  nodes.py                # Graph nodes and routing logic
  service.py              # Stateful handle_message API
  state.py                # Graph state schema
  tools.py                # Agent tools
  rag/                    # RAG ingestion and retrieval
  scheduling/             # SQLite interview slot storage
  telegram_bot/           # Telegram long polling interface

data/
  hr_docs/                # HR knowledge base markdown files

datasets/                 # LangSmith evaluation datasets
langgraph.json            # LangGraph Studio config
requirements.txt
pyproject.toml
```

## Environment

Create `.env` in the project root:

```bash
OPENROUTER_API_KEY=<your-openrouter-key>
OPENROUTER_MODEL=google/gemini-3-flash-preview

LANGSMITH_API_KEY=<your-langsmith-key>
LANGSMITH_PROJECT=hr_agent
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com

TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
HF_TOKEN=<optional-huggingface-token>
```

`HF_TOKEN` is optional for public models, but it can improve Hugging Face download reliability and rate limits.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you use an existing Python environment, install the same requirements there.

## Prepare RAG Index

The HR knowledge base is stored in `data/hr_docs`. To build the local Chroma index:

```bash
HF_HOME="$PWD/.cache/huggingface" \
HF_HUB_DISABLE_XET=1 \
python -m hr_agent_app.rag.ingest
```

The vector store is created in:

```text
.vectorstore/chroma
```

Both `.cache/` and `.vectorstore/` are ignored by git.

At query time, `search_hr_documents` uses HyDE: the LLM first drafts a short hypothetical answer to the candidate's question, and the retriever searches the vector store with this expanded query. If HyDE generation fails, retrieval falls back to the original question.

## Prepare Interview Slots

Create the local SQLite database and seed sample interview slots:

```bash
python -m hr_agent_app.scheduling.seed
```

The database is stored as:

```text
data/hr_agent.db
```

It is ignored by git.

## Run Locally

### CLI

```bash
python -m hr_agent_app.cli
```

### LangGraph Studio

```bash
langgraph dev
```

Open the Studio URL printed by the command. The graph id is `hr_agent`.

### Telegram Bot

Create a bot with BotFather, add `TELEGRAM_BOT_TOKEN` to `.env`, then run:

```bash
python -m hr_agent_app.telegram_bot.bot
```

Supported commands:

```text
/start - start interview
/reset - reset current session
/help  - show help
```

## Example Interaction

```text
User: /start
Bot: Здравствуйте! Я HR-бот для первичного интервью в ML-команду...

User: Какие этапы интервью?
Bot: Процесс отбора обычно состоит из первичного HR-скрининга,
     технического интервью, финального интервью, обсуждения оффера
     и обратной связи.
     Источник: hiring_process.md

User: Покажи свободные слоты для интервью
Bot: Свободные слоты для интервью:
     2. 2026-05-27T15:00-2026-05-27T16:00 Europe/Moscow...

User: Забронируй слот 2 на Павла, pavel@example.com
Bot: Слот успешно забронирован...
```

## Evaluation

The project includes LangSmith datasets for testing core behavior:

- `hr_agent_role_tests` checks final role classification.
- `hr_agent_dialog_policy_tests` checks re-asking behavior and guardrail responses.

Example local experiment command:

```bash
python scripts/run_langsmith_policy_experiment.py
```

## Notes

- The current scheduling module is an MVP using SQLite. It can later be replaced with Google Calendar, Calendly, or an ATS/CRM integration without changing the agent-facing tool interface.
- RAG uses local markdown files and a local Chroma index. This keeps the demo reproducible and does not require a separate vector database service.
- The Telegram bot uses long polling for local development. A production deployment would usually use webhook mode.
