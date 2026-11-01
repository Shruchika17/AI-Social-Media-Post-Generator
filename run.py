"""
run.py — Entry point that starts both the FastAPI backend and Streamlit frontend.

Usage:
    python run.py

The FastAPI server starts on http://localhost:8000
The Streamlit UI  starts on http://localhost:8501
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

# Force utf-8 encoding on standard output for Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure we run from the project root so relative imports work
os.chdir(Path(__file__).parent)


def stream_output(proc: subprocess.Popen, prefix: str):
    """Stream stdout from a subprocess with a readable prefix."""
    for line in iter(proc.stdout.readline, b""):
        try:
            print(f"[{prefix}] {line.decode('utf-8', errors='replace').rstrip()}", flush=True)
        except Exception:
            pass


def main():
    print("=" * 60)
    print("[*] AI Social Media Post Generator")
    print("=" * 60)
    print()

    processes = []

    # ── Start FastAPI backend ──────────────────────────────────────
    print("[+] Starting FastAPI backend on http://localhost:8000 ...")
    api_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    processes.append(api_proc)
    threading.Thread(target=stream_output, args=(api_proc, "API"), daemon=True).start()

    # Give the API a moment to start before launching the UI
    time.sleep(3)

    # ── Start Streamlit frontend ────────────────────────────────────
    print("[+] Starting Streamlit UI on http://localhost:8502 ...")
    ui_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py",
         "--server.port", "8502",
         "--server.address", "0.0.0.0",
         "--browser.gatherUsageStats", "false"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    processes.append(ui_proc)
    threading.Thread(target=stream_output, args=(ui_proc, "UI"), daemon=True).start()

    print()
    print("[OK] Both services started!")
    print("   -> API:  http://localhost:8000")
    print("   -> Docs: http://localhost:8000/docs")
    print("   -> UI:   http://localhost:8502")
    print()
    print("Press Ctrl+C to stop both services.")
    print("=" * 60)

    def shutdown(sig, frame):
        print("\n⏹  Shutting down...")
        for p in processes:
            p.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Keep alive until both processes exit
    for p in processes:
        p.wait()


if __name__ == "__main__":
    main()
