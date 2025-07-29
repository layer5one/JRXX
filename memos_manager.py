import json
import uuid
from MemoryOS import MOS
from MemoryOS.configs.mem_os import MOSConfig

class MemOSManager:
    def __init__(self, session_id: str, config_path: str, scratchpad_template: str, codex_template: str):
        self.session_id = session_id
        self.mos_config = MOSConfig(config_path=str(config_path))
        self.scratchpad_template_path = scratchpad_template
        self.codex_template_path = codex_template
        self.client = None

    def connect(self):
        """Establishes connection to the MOS server and registers cubes."""
        try:
            self.client = MOS(self.mos_config)
            self.client.create_user_profile(user_id=self.session_id)
            
            self.client.register_mem_cube(str(self.scratchpad_template_path), user_id=self.session_id, mem_id="scratchpad_mem")
            self.client.register_mem_cube(str(self.codex_template_path), user_id=self.session_id, mem_id="codex_mem")
            print(f"MemOS connection established for session {self.session_id}")
        except Exception as e:
            print(f"FATAL: Could not connect to MemOS server. Is it running? Error: {e}")
            raise ConnectionError("Failed to connect to MemOS server.")


    def update_scratchpad(self, state_update: dict):
        """Writes or updates the state in the Scratchpad MemCube."""
        current_state = self.read_scratchpad()
        current_state.update(state_update)
        message = {"role": "system", "content": json.dumps(current_state)}
        self.client.add_memory(messages=[message], user_id=self.session_id, mem_id="scratchpad_mem")

    def read_scratchpad(self) -> dict:
        """Reads the entire content of the current session's Scratchpad."""
        try:
            memory_content = self.client.search_memory(query="*", user_id=self.session_id, mem_id="scratchpad_mem")
            if memory_content and memory_content.get('text_mem'):
                return json.loads(memory_content['text_mem'][-1]['content'])
            with open(self.scratchpad_template_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read scratchpad. Returning template. Error: {e}")
            with open(self.scratchpad_template_path, 'r') as f:
                return json.load(f)


    def add_lesson_to_codex(self, problem_signature: str, failure_pattern: list, successful_resolution: list, human_guidance: str):
        """Writes a new, permanent lesson to the Codex MemCube."""
        lesson = {
            "lesson_id": str(uuid.uuid4()),
            "problem_signature": problem_signature,
            "failure_pattern": failure_pattern,
            "successful_resolution": successful_resolution,
            "human_guidance": human_guidance,
            "confidence_score": 0.95
        }
        message = {"role": "system", "content": json.dumps(lesson)}
        self.client.add_memory(messages=[message], user_id=self.session_id, mem_id="codex_mem")
        print(f"New lesson '{problem_signature}' added to Codex.")

    def search_codex(self, error_description: str) -> list[dict]:
        """Performs a semantic search on the Codex for previously solved problems."""
        print(f"Searching Codex for solutions to: '{error_description}'")
        try:
            results = self.client.search_memory(query=error_description, user_id=self.session_id, mem_id="codex_mem")
            if results and results.get('text_mem'):
                return [json.loads(mem['content']) for mem in results['text_mem']]
            return []
        except Exception as e:
            print(f"Warning: Could not search codex. Error: {e}")
            return []
