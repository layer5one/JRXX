import argparse
import sys
from config import AgentState, MemOSConfig
from graph import JaraxxusGraph
import memos_manager

def main():
    parser = argparse.ArgumentParser(description="Jaraxxus Agentic System")
    parser.add_argument("--session-id", required=True, help="The unique ID for this task session.")
    parser.add_argument("--task", required=True, help="The task description for the agent.")
    parser.add_argument("--recovering-from-crash", action="store_true", help="Flag to indicate a recovery boot sequence.")
    args = parser.parse_args()

    try:
        memos = memos_manager.MemOSManager(
            session_id=args.session_id,
            config_path=MemOSConfig.CONFIG_PATH,
            scratchpad_template=MemOSConfig.SCRATCHPAD_TEMPLATE_PATH,
            codex_template=MemOSConfig.CODEX_TEMPLATE_PATH
        )
        memos.connect()
    except ConnectionError as e:
        print(f"Could not start Jaraxxus: {e}")
        sys.exit(1)


    jaraxxus_app = JaraxxusGraph(memos).graph

    initial_state = AgentState(
        session_id=args.session_id,
        task=args.task,
        plan=[],
        trace=[{"state": "start", "task": args.task}],
        error=False,
        error_message="",
        failed_action={},
        is_novel_error=False,
        human_feedback="",
        progenitor_query=""
    )
    
    if args.recovering_from_crash:
        print("!!! RECOVERY MODE ACTIVATED !!!")
        initial_state['error'] = True
        scratchpad = memos.read_scratchpad()
        initial_state['failed_action'] = scratchpad.get('failed_action', {})
        initial_state['error_message'] = scratchpad.get('crash_log', 'Unknown crash')
        initial_state['trace'] = scratchpad.get('trace', [])
    else:
        memos.update_scratchpad(initial_state)
    
    # Run the graph
    for s in jaraxxus_app.stream(initial_state, config={"recursion_limit": 150}):
        # Status is printed within the graph nodes for better real-time feedback
        pass

    print("\n---JARAXXUS TASK COMPLETE---")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("This script is intended to be run by watchdog.sh")
        print("Usage: ./watchdog.sh \"<your task>\"")
    else:
        main()
