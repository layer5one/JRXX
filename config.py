import os
from pathlib import Path
from typing import TypedDict, List, Dict, Any

# --- PATHS ---
BASE_DIR = Path(__file__).parent.resolve()
CONFIG_DIR = BASE_DIR / "config"
PERSONAS_DIR = BASE_DIR / "personas"

# --- AGENT CONFIG ---
class AgentConfig:
    ORCHESTRATOR_MODEL = "gemma3:12b-it-qat"
    CODE_SPECIALIST_MODEL = "jaraxxus-code-agent:latest"
    FILE_IO_SPECIALIST_MODEL = "jaraxxus-file-agent:latest"

# --- MEMOS CONFIG ---
class MemOSConfig:
    CONFIG_PATH = CONFIG_DIR / "memos_config.json"
    SCRATCHPAD_TEMPLATE_PATH = CONFIG_DIR / "scratchpad_template.json"
    CODEX_TEMPLATE_PATH = CONFIG_DIR / "codex_template.json"

# --- LANGGRAPH STATE ---
class AgentState(TypedDict):
    """
    Represents the state of our graph. This is the operational memory
    that flows between the nodes of the agent's thought process.
    """
    session_id: str
    task: str
    plan: List[Dict[str, str]]
    trace: List[Dict]
    error: bool
    error_message: str
    failed_action: Dict
    is_novel_error: bool
    human_feedback: str
    progenitor_query: str
