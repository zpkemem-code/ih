#!/bin/bash

# Start FastAPI app in background
uvicorn app:app --host 0.0.0.0 --port 5000 &

UVICORN_PID=$!

# Wait for FastAPI to start
sleep 2

# Run the Zohun bot
python -m Zohun

# Cleanup
kill $UVICORN_PID 2>/dev/null || true
