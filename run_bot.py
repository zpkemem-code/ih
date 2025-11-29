#!/usr/bin/env python3
import os
import sys
import subprocess
import signal

def signal_handler(sig, frame):
    print("Shutting down...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, "-m", "Zohun"])
