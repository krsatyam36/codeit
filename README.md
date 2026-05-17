# ⚡ Codeit // Local AI Research Compiler & Sandbox IDE

**Research to Code Engine:** Transform academic research papers, mathematical text, and complex algorithms directly into executable PyTorch code—completely offline. Codeit features a built-in Split-Pane IDE and an Ephemeral Execution Sandbox to safely auto-resolve dependencies and run AI-generated code on your local hardware.

---

## 🚀 Core Architecture & Features

* **Ephemeral Execution Sandbox:** A production-grade security and execution layer. Codeit uses Python's Abstract Syntax Tree (`ast`) to parse LLM-generated code, rips out the `import` statements, spins up a temporary isolated `venv`, auto-installs PyPI dependencies, executes the script with strict timeouts, and safely destroys the environment.
* **Interactive Split-Pane IDE:** Say goodbye to raw JSON dumps. Watch the LLM stream pure Python into a sleek, dark-themed code editor. Edit and tweak the generated code in real-time before hitting "Run".
* **Live Terminal Console:** Standard output and execution errors from the isolated sandbox are piped back into the browser's terminal pane in real-time.
* **Dynamic Local Model Routing:** Automatically detects your local Ollama roster. Hot-swap between powerhouse models like `qwen2.5-coder:14b-instruct`, `deepseek-r1:14b`, `codestral`, and `llama3.2` directly from the UI dropdown.
* **100% Privacy-First:** Powered entirely by local compute. Zero API keys, zero cloud latency, and zero data leaks. 
* **Dual Input Processing:** Drag-and-drop local PDF documents (up to 25MB) or paste a direct arXiv URL to dynamically scrape target papers.

## 🛠️ Tech Stack

* **Backend Orchestration:** Python, FastAPI, Uvicorn
* **Execution Engine:** Python `ast`, `venv`, `subprocess`, `tempfile`
* **Document Processing:** PyMuPDF (`fitz`), `httpx` (for arXiv integration)
* **AI Engine:** Local Ollama REST API
* **Frontend:** HTML5, Tailwind CSS, Vanilla JS, Server-Sent Events (SSE)
* **CLI Wrapper:** Click

## 📦 Prerequisites

Ensure your local machine is prepped with:
1. **Python 3.10+**
2. **Ollama** (running locally on port `11434`)
3. At least one capable coding model pulled locally (e.g., `ollama run qwen2.5-coder:14b-instruct`)

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/krsatyam36/codeit.git](https://github.com/krsatyam36/codeit.git)
   cd codeit

    Set up a virtual environment:
    Bash

    python3 -m venv venv
    source venv/bin/activate

    Install the package and dependencies:
    Bash

    pip install -e .

💻 Usage

Spin up the local compiler and IDE using the built-in CLI:
Bash

codeit serve

The system will initialize the Uvicorn server and bind to http://localhost:8080. Custom ports can be specified via codeit serve --port 8081.
📁 Project Structure
Plaintext

codeit/
├── codeit/
│   ├── __init__.py
│   ├── cli.py                 # CLI interface setup
│   ├── main.py                # FastAPI routes, AST sandboxing, and SSE streaming
│   ├── services/
│   │   ├── sandbox_engine.py  # Ephemeral venv creation & dependency resolution
│   │   ├── ollama_client.py   # Local LLM streaming integration
│   │   └── pdf_processor.py   # PyMuPDF extraction & arXiv logic
│   └── templates/
│       └── index.html         # Split-Pane IDE and Terminal UI
├── requirements.txt
├── setup.py
└── README.md

🤝 Contributing

Contributions, issues, and feature requests are always welcome.
📝 License

Distributed under the MIT License.
