import sys
import os
from pathlib import Path

# Configure utf-8 encoding for standard output if supported
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend directory to sys.path and set working directory
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))
os.chdir(str(backend_dir))

if __name__ == "__main__":
    import threading
    import uvicorn
    from app.core.config import settings
    from app.db.seed import seed_database
    
    # Determine port: from CLI argument, or PORT env variable, defaulting to 5000
    port = 5000
    HOST = os.environ.get("HOST", "127.0.0.1")  # bind to localhost by default; set HOST=0.0.0.0 to share on your LAN
    for arg in sys.argv[1:]:
        if arg.isdigit():
            port = int(arg)
            break
        elif arg.startswith("--port="):
            port = int(arg.split("=")[1])
            break
    if "PORT" in os.environ and os.environ["PORT"].isdigit():
        port = int(os.environ["PORT"])

    print("=" * 65)
    print("[*] Starting TalentPulse AI Enterprise Platform...")
    print("[*] Visakhapatnam IT Services Center")
    print(f"[*] Primary Port:   http://localhost:{port}/ui")
    if port != 8000:
        print(f"[*] Auxiliary Port: http://localhost:8000/ui (Dual Sync)")
    print("=" * 65)
    
    # Auto-seed database if needed
    try:
        seed_database()
    except Exception as e:
        print(f"Database check completed ({e}).")

    print(f"\n[+] Web Portal:    http://localhost:{port}/ui (and http://localhost:8000/ui)")
    print(f"[+] DB Explorer:   http://localhost:{port}/db")
    print(f"[+] API Docs:       http://localhost:{port}/docs")
    print(f"[+] Health Status:  http://localhost:{port}/health\n")

    # Start auxiliary listener on port 8000 if different so existing browser tabs remain 100% in sync
    if port != 8000:
        def start_aux():
            try:
                uvicorn.run("app.main:app", host=HOST, port=8000, log_level="warning")
            except Exception:
                pass
        threading.Thread(target=start_aux, daemon=True).start()

    uvicorn.run("app.main:app", host=HOST, port=port, reload=False)
