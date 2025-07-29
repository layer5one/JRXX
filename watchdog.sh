#!/bin/bash

# The watchdog process responsible for monitoring and restarting the Jaraxxus agent.

# Check if a task was provided
if [ -z "$1" ]; then
  echo "Usage: $0 \"<task_description>\""
  exit 1
fi

TASK_DESCRIPTION="$1"
SESSION_ID=$(python -c 'import uuid; print(uuid.uuid4())')
PID_FILE="/tmp/jaraxxus_${SESSION_ID}.pid"
LOG_FILE="/tmp/jaraxxus_${SESSION_ID}.log"

# Function to start the agent
start_agent() {
  echo "Starting Jaraxxus for session ${SESSION_ID}..."
  # Start the main python script in the background
  python jaraxxus.py --session-id "$SESSION_ID" --task "$TASK_DESCRIPTION" "$@" > "$LOG_FILE" 2>&1 &
  # Store the process ID
  echo $! > "$PID_FILE"
}

# Initial start
start_agent

while true; do
  # Check if the process ID in the file exists and is running
  if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null; then
    # Process is running, sleep and check again
    sleep 5
    continue
  fi

  echo "Jaraxxus process crashed or has finished."

  # Check if the log file has content before attempting to log a crash
  if [ -s "$LOG_FILE" ]; then
      echo "Logging crash to MemOS..."
      CRASH_LOG_CONTENT=$(cat "$LOG_FILE")

      # Pass the log content as a command-line argument to the Python script.
      python -c "
import sys
sys.path.append('.') # Add current directory to Python's path to find modules.
import memos_manager
import json
from config import MemOSConfig

crash_log = sys.argv[1]
session_id = sys.argv[2]

manager = memos_manager.MemOSManager(
    session_id=session_id,
    config_path=MemOSConfig.CONFIG_PATH,
    scratchpad_template=MemOSConfig.SCRATCHPAD_TEMPLATE_PATH,
    codex_template=MemOSConfig.CODEX_TEMPLATE_PATH
)
manager.connect()
crash_state = {'crash_log': crash_log}
manager.update_scratchpad(crash_state)
print('Crash log written to Scratchpad.')
" "$CRASH_LOG_CONTENT" "$SESSION_ID"

  fi

  # Restart the agent in recovery mode
  echo "Restarting in recovery mode..."
  start_agent --recovering-from-crash
  
  # Add a longer sleep after a crash to prevent rapid-fire restarts
  sleep 10
done

# Cleanup function to run when the watchdog script itself is terminated
trap "echo 'Stopping watchdog and Jaraxxus...'; kill \$(cat \"$PID_FILE\") 2>/dev/null; rm -f \"$PID_FILE\"; exit 0" SIGINT SIGTERM
