import subprocess
import json
from config import AgentConfig

class LLMManager:
    """
    A manager to handle all model interactions via Simon Willison's `llm` library.
    This is the core execution engine for the Orchestrator and local Specialists.
    It has NO knowledge of the Progenitor.
    """
    def _execute_llm_command(self, command: list) -> str:
        """A robust wrapper for running `llm` CLI commands."""
        try:
            print(f"---LLMManager executing: {' '.join(command)}---")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=180
            )
            return result.stdout.strip()
        except FileNotFoundError:
            return '{"error": "llm command not found. Is it installed and in your PATH?"}'
        except subprocess.CalledProcessError as e:
            error_details = json.dumps(e.stderr.strip())
            return f'{{"error": "LLM command failed", "details": {error_details}}}'
        except Exception as e:
            return f'{{"error": "An unexpected error occurred", "details": "{str(e)}"}}'

    def run_orchestrator(self, prompt: str, system_prompt: str) -> dict:
        """
        Runs the main orchestrator for planning and reflection, ensuring JSON output.
        """
        command = [
            'llm',
            '-m', AgentConfig.ORCHESTRATOR_MODEL,
            '-s', system_prompt,
            prompt
        ]
        response_str = self._execute_llm_command(command)
        try:
            json_start = response_str.find('{')
            json_end = response_str.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                return json.loads(response_str[json_start:json_end])
        except json.JSONDecodeError:
            print(f"Orchestrator did not return valid JSON: {response_str}")
            return {"error": "Invalid JSON response", "raw": response_str}
        return {"error": "No JSON found in response"}


    def run_specialist_with_tools(self, specialist_model: str, task: str) -> dict:
        """
        Runs a specialist agent to perform a task by calling a tool.
        """
        command = [
            'llm', '-m', specialist_model,
            '-s', "You are a specialist agent. Your only goal is to solve the task by calling exactly one tool. Respond with ONLY the tool call's JSON output.",
            task,
            '--tool', 'tools:read_file',
            '--tool', 'tools:write_file',
            '--tool', 'tools:execute_shell',
            '--no-stream'
        ]

        response_str = self._execute_llm_command(command)
        try:
            response_json = json.loads(response_str)
            if isinstance(response_json, list) and response_json:
                return response_json[0]
            return {"error": "Tool call returned empty or invalid list."}
        except json.JSONDecodeError:
            return {"error": "Failed to decode JSON from specialist tool call.", "raw": response_str}

# Create a single instance to be used across the application
llm_manager = LLMManager()
