import os

APP_PORT = 45667
FRONT_END = "http://localhost:3000"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not set, configure it as an environment variable using 'export OPENAI_API_KEY=...'.")

# Agent
MAX_HISTORY_LEN = 20
