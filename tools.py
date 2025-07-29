import os
import subprocess

# Simple, callable Python functions that the `llm` library will
# discover and execute as tools.

def read_file(file_path: str) -> str:
    """Reads the entire content of a file and returns it as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(file_path: str, content: str) -> str:
    """Writes the given content to a file, overwriting it if it exists."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File '{file_path}' written successfully."
    except Exception as e:
        return f"Error writing file: {e}"

def execute_shell(command: str) -> str:
    """
    Executes a shell command and returns its combined stdout and stderr.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )
        if result.returncode != 0:
            return f"Error (Exit Code {result.returncode}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Execution failed: {str(e)}"
