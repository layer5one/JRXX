import subprocess
import os

# This module handles the strategic invocation of the Gemini Progenitor.
# It uses the CORRECT `google-gemini/gemini-cli` tool.
# The command structure is `gemini prompt [flags] [prompt_text]`

def invoke_progenitor(prompt: str, context_files: list[str] = None) -> str:
    """
    Correctly invokes the `gemini-cli` tool using the `prompt` command.
    """
    command = ['gemini', 'prompt']
    
    if context_files:
        for file in context_files:
            if os.path.exists(file):
                command.extend(['--context-file', file])
            else:
                print(f"[Warning] Progenitor context file not found: {file}")

    command.append(prompt)

    try:
        print("---INVOKING GEMINI PROGENITOR (google-gemini/gemini-cli)---")
        print(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=300)
        print("---PROGENITOR RESPONSE RECEIVED---")
        return result.stdout.strip()
    except FileNotFoundError:
        error_msg = "Error: `gemini` command not found. Is the google-gemini/cli installed and in your PATH?"
        print(error_msg)
        return error_msg
    except subprocess.CalledProcessError as e:
        error_msg = f"Error invoking Gemini Progenitor: {e.stderr}"
        print(error_msg)
        return f"Progenitor invocation failed: {e.stderr}"
    except subprocess.TimeoutExpired:
        error_msg = "Error: Gemini Progenitor invocation timed out."
        print(error_msg)
        return error_msg


def design_new_tool(request: str) -> str:
    """Trigger 1: Designs a new Python tool."""
    prompt = f"""
Design a new Python tool for my toolset. The tool must be a single function
with type hints and a clear docstring. The request is: '{request}'
The tool must follow best practices and include error handling.
Return ONLY the complete Python code for the function. Do not include any other text or markdown fences.
"""
    return invoke_progenitor(prompt, context_files=['tools.py'])

def refactor_architecture(bottleneck_analysis: str, code_modules: list[str]) -> str:
    """Trigger 2: Proposes an architectural refactoring."""
    prompt = f"""
I am a self-improving coding agent. A performance analysis indicates a significant bottleneck: {bottleneck_analysis}.
The relevant source code modules are provided in the context.
Propose a specific, non-destructive modification to my own code to improve this bottleneck.
Provide the change in the standard `diff` format ONLY.
"""
    return invoke_progenitor(prompt, context_files=code_modules)

def analyze_unsolvable_error(failure_logs: list[str]) -> str:
    """Trigger 3: Analyzes a recurring, unsolvable error."""
    logs = "\n\n".join(failure_logs)
    prompt = f"""
I am an AI agent stuck in a recovery loop. My reasoning seems to be flawed.
Here are the logs from several consecutive failed attempts:
---
{logs}
---
Analyze this recurring failure pattern and identify the fundamental flaw in my approach.
Do not provide code. Provide a concise, high-level strategic change to my problem-solving methodology for this class of problem.
"""
    return invoke_progenitor(prompt)
