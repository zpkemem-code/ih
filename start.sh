#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PORT=$(python3 -c "import socket; p = next((p for p in range(7860, 7960) if socket.socket().connect_ex(('localhost', p)) != 0), None); print(p)")

python3 -m uvicorn app:app --host 0.0.0.0 --port $PORT &
UVICORN_PID=$!

python3 -m Zohun

kill $UVICORN_PID 2>/dev/null
