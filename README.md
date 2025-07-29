# Jaraxxus Agentic System (Corrected Architecture)

This project implements the Jaraxxus agentic system, a truly autonomous agent capable of self-healing and self-improvement. This version has been completely reviewed and corrected to adhere to the original architectural blueprint.

## Core Architecture

* **Hierarchical Agents:** An Orchestrator (`gemma3:12b-it-qat`) manages high-level strategy, delegating tasks to specialized agents.
* **Dual Execution Engines:** The system uses two distinct, specialized command-line interfaces for model interaction:
    1.  **`llm` CLI:** The primary engine for all local model interactions (Orchestrator, Specialists via Ollama).
    2.  **`gemini` CLI:** The dedicated "escape hatch" for invoking the Gemini Progenitor for high-level, codebase-aware strategic guidance.
* **Stateful Orchestration:** `LangGraph` remains the backbone for the agent's stateful workflow, enabling complex logic for error recovery and learning.
* **Persistent Memory (MemOS):** The agent's consciousness is powered by MemOS, with the "Scratchpad" for operational state and the "Codex" for learned lessons.
* **Self-Healing & Self-Improvement:** The "Reflect-Learn-Act" cycle is preserved, with the `watchdog` process detecting crashes and triggering the recovery and learning protocols.

## Setup and Installation

### 1. System-Level Prerequisites (Non-Python)

Before installing Python packages, ensure these tools are installed, configured, and available in your system's `PATH`.

* **Node.js and npm:** Required to install the `google-gemini/cli`.
* **Gemini CLI:** Install the official Google Gemini CLI globally via npm.
    ```bash
    npm install -g @google/gemini-cli
    ```
    After installation, configure it by authenticating with your Google account:
    ```bash
    gemini auth
    ```
* **Ollama:** Install and run the Ollama service. See [ollama.com](https://ollama.com/).
* **MemOS:** Install and run the MemoryOS server. Follow the instructions at its official repository.

### 2. Python Environment and Dependencies

1.  **Create the directory structure and save all the provided files.**
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install Python dependencies from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure the `llm` CLI:**
    ```bash
    # This ensures the llm command can see your Ollama models
    llm ollama
    ```

### 3. Model Setup

1.  **Pull Ollama Base Models:**
    ```bash
    ollama pull gemma3:12b-it-qat
    ollama pull qwen3:8b
    ollama pull gemma3n:e4b-it-qat
    ```
2.  **Create Custom Persona Models with Ollama:**
    ```bash
    ollama create jaraxxus-code-agent -f ./personas/CodePersona.Modelfile
    ollama create jaraxxus-file-agent -f ./personas/FileIOPersona.Modelfile
    ```

### 4. Final Configuration

* Update `config/memos_config.json` to point to your running MemOS server.

## Running the System

The system is managed by `watchdog.sh` for resilience.

To start a new task:
```bash
chmod +x watchdog.sh
./watchdog.sh "Your complex task description here."
