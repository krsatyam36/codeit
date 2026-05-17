# ⚡ Codeit // Local AI Research Compiler & Sandbox IDE

**Research to Code Engine:** Transform academic research papers, mathematical text, and complex ML algorithms directly into executable PyTorch script matrices—completely offline. Codeit pairs an interactive Split-Pane Workspace with an Ephemeral Execution Sandbox to safely parse dependencies, install required packages, and run local inference pipelines on your hardware.

---

## 🚀 Core Architecture & Features

* **Ephemeral Execution Sandbox:** A robust execution and security layer. Codeit uses Python's Abstract Syntax Tree (`ast`) to inspect LLM-generated code dynamically, extracts all unique `import` statements, builds a short-lived isolated virtual environment (`venv`), auto-resolves and installs PyPI packages, executes the script via a strict-timeout subprocess, and completely destroys the environment post-execution.
* **Interactive Split-Pane Workspace:** Watch your model stream pure, unstructured Python code live into a dark-themed text editor. Tweak, edit, or append logic manually in the workspace to fix parsing errors before execution.
* **Sandbox Execution Console:** Tracks standard output and exceptions streamed straight from the isolated sandbox environment, providing live runtime feedback in the browser terminal layout.
* **Dynamic Local Model Grid:** Completely integrated to route prompts across your machine's unique active Ollama roster. Seamlessly hot-swap weights right from the dropdown matrix:
  * **Optimized Programming Models:** `qwen2.5-coder:14b-instruct` (Primary Engine), `qwen2.5-coder:latest`, `codestral:latest`
  * **Advanced Reasoning & Large Foundation Weights:** `deepseek-r1:14b`, `deepseek-r1:latest`, `qwen3:14b`, `qwen2.5:14b`, `gpt-oss:20b`, `mistral-small:latest`
  * **Multimodal Vision & Lightweight Weights:** `llama3.2-vision:11b`, `llama3.2-vision:latest`, `llama3.2:latest`, `gemma3:latest`, `gemma3:4b`, `minicpm-v:latest`, `qwen2.5vl:7b`, `llava:7b`, `hermes3:8b`
* **100% Privacy-Preserving:** Operates fully on internal loops. Zero API keys, zero outbound network dependencies, and zero data leaks.

## 🛠️ Tech Stack

* **Backend Engine:** Python, FastAPI, Uvicorn
* **Sandbox Runtime:** Python `ast`, `venv`, `subprocess`, `tempfile`
* **Document Extraction:** PyMuPDF (`fitz`), `httpx` (for dynamic arXiv parsing)
* **AI Fabric:** Ollama Local REST Client API
* **Frontend Matrix:** HTML5, Tailwind CSS, Vanilla JavaScript, Server-Sent Events (SSE)
* **Control CLI:** Click

## 📦 Prerequisites

Before deploying the local service node, confirm your system matches this state:
1. **Python 3.10+** installed on the host.
2. **Ollama Server** active and bound to port `11434`.
3. Target architecture weights pulled locally (e.g., `ollama run qwen2.5-coder:14b-instruct`).

## ⚙️ Installation & Launch

1. **Clone the local repository:**
   ```bash
   git clone [https://github.com/krsatyam36/codeit.git](https://github.com/krsatyam36/codeit.git)
   cd codeit

    Initialize local virtual environment:
    Bash

    python3 -m venv venv
    source venv/bin/activate

    Install the package in editable/development state:
    Bash

    pip install -e .

    Launch the processing node service:
    Bash

    codeit serve

    The runtime binds to http://127.0.0.1:8080 by default. Override port bindings using codeit serve --port <port_number> if a socket clash occurs.

📁 Project Structure
Plaintext

codeit/
├── codeit/
│   ├── __init__.py
│   ├── cli.py                 # CLI interface controller
│   ├── main.py                # FastAPI routing matrix and execution entrypoints
│   ├── services/
│   │   ├── sandbox_engine.py  # Ephemeral sandbox creation, AST mapping, & execution
│   │   ├── ollama_client.py   # Context composition and Ollama REST streaming
│   │   └── pdf_processor.py   # PyMuPDF ingestion and arXiv web scraping
│   └── templates/
│       └── index.html         # Interactive Split-Pane Workspace & UI Layout
├── requirements.txt
├── setup.py
└── README.md

📝 License

Distributed under the MIT License.
