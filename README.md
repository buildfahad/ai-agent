# AI Agent 🤖

A terminal-based autonomous coding agent powered by Google Gemini. Give it a task in plain English and it figures out what to do — reading files, writing code, and running Python — on its own, in a loop, until the job is done.

Built from scratch to understand how tools like Cursor and Claude Code work under the hood.

---

## How It Works

```
You type a prompt
        ↓
Agent sends it to Gemini 2.5 Flash with a system prompt + tool declarations
        ↓
Gemini decides which tool to call (read file, write file, run code, list directory)
        ↓
Agent executes the tool and feeds the result back to Gemini
        ↓
Loop repeats up to 20 iterations until Gemini responds with no tool calls
        ↓
Final answer printed to terminal
```

This is the same core agentic loop used by Claude Code, Cursor, and Devin — the model drives, the tools execute.

---

## Features

- **Autonomous agentic loop** — runs up to 20 iterations, calling tools and reasoning over results until the task is complete
- **File system tools** — list directory contents, read files, write/overwrite files
- **Code execution** — runs Python files and feeds stdout/stderr back to the model
- **Verbose mode** — see every tool call and result as it happens
- **Full conversation history** — the entire message thread is maintained across iterations so the model has complete context

---

## Tools Available to the Agent

| Tool | What It Does |
|---|---|
| `get_files_info` | List files and metadata in a directory |
| `get_file_content` | Read the contents of a file |
| `write_file` | Write or overwrite a file |
| `run_python_file` | Execute a Python file and capture output |

---

## Tech Stack

- Python 3
- Google Gemini API (`google-genai`)
- `uv` for dependency management
- `python-dotenv` for environment variables

---

## Getting Started

**Prerequisites:** Python 3.10+, a Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

**1. Clone the repo**
```bash
git clone https://github.com/buildfahad/ai-agent.git
cd ai-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
# or with uv:
uv sync
```

**3. Set up your API key**

Create a `.env` file in the root:
```
GEMINI_API_KEY1=your_key_here
```

**4. Run the agent**
```bash
python main.py "fix the bug in calculator.py"
```

Add `--verbose` to see every tool call:
```bash
python main.py "add error handling to main.py" --verbose
```

---

## Project Structure

```
ai-agent/
├── main.py               # Agent loop and CLI entry point
├── call_function.py      # Tool dispatcher — maps model calls to Python functions
├── prompts.py            # System prompt defining agent behavior
├── config.py             # Configuration
├── functions/
│   ├── get_files_info.py     # List directory contents
│   ├── get_file_content.py   # Read file contents
│   ├── write_file.py         # Write/overwrite files
│   └── run_python_file.py    # Execute Python files
├── calculator/           # Example project for the agent to work on
└── tests/                # Tool unit tests
```

---

## Architecture Notes

**Why a loop up to 20 iterations?** A single model call can't complete multi-step tasks — it needs to call a tool, see the result, then decide what to do next. The loop lets the model work iteratively the same way a human developer would.

**Why keep the full message history?** Without it the model loses context between tool calls and can't reason about what it already did. Every tool call and result is appended to the messages list so the model always has the full picture.

**Tool declarations separate from the dispatcher** — `call_function.py` maps model-requested function names to actual Python callables. This separation makes it easy to add new tools without touching the agent loop.

**Working directory is hardcoded** — intentionally scoped to the `calculator/` folder while the project is in early development. Giving an AI agent unrestricted file system access without proper sandboxing is a real security concern.
---

## Built By

Fahad — self-taught developer  
Learning backend engineering via [Boot.dev](https://boot.dev) | Previously: CS50
