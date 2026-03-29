import os
import sys
import subprocess
import venv
from pathlib import Path

# --- CONFIGURATION ---
VENV_DIR = Path(".venv")
REQUIREMENTS = "requirements.txt"
APP_MODULE = "src.main:app"  # Adjust if your entry point is different
PORT = 8000


def get_python_executable():
    """Returns the path to the python binary inside the venv."""
    if os.name == "nt":  # Windows
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run_command(command, description):
    """Helper to run shell commands and handle errors."""
    print(f"--- {description} ---")
    try:
        # Use shell=True on Windows if command is a string,
        # but list is safer for subprocess.
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed: {e}")
        sys.exit(1)


def setup_venv():
    """Creates venv if it doesn't exist."""
    if not VENV_DIR.exists():
        print(f"--- Creating Virtual Environment in {VENV_DIR} ---")
        venv.create(VENV_DIR, with_pip=True)

    python_bin = str(get_python_executable())

    # Update pip and install requirements
    if Path(REQUIREMENTS).exists():
        run_command([python_bin, "-m", "pip", "install", "--upgrade", "pip"], "Updating Pip")
        run_command([python_bin, "-m", "pip", "install", "-r", REQUIREMENTS], "Installing Dependencies")


def main():
    # 1. Setup/Activate environment logic
    setup_venv()
    python_bin = str(get_python_executable())

    # 2. Run Alembic Migrations
    # This ensures your DB schema matches your models before the app starts
    if Path("alembic.ini").exists():
        # We call alembic through the venv's python to ensure it uses the right libs
        run_command([python_bin, "-m", "alembic", "upgrade", "head"], "Running Database Migrations")
    else:
        print("--- Skipping Migrations (alembic.ini not found) ---")

    # 3. Start FastAPI with Uvicorn
    # We use 'python -m uvicorn' to ensure it runs from the venv
    uvicorn_cmd = [
        python_bin, "-m", "uvicorn",
        APP_MODULE,
        "--host", "0.0.0.0",
        "--port", str(PORT),
        "--reload",  # Remove this in production Dockerfiles
        "--ssl-keyfile", "./localhost+2-key.pem",  # Path to your private key
        "--ssl-certfile", "./localhost+2.pem"
    ]

    run_command(uvicorn_cmd, f"Starting FastAPI on Port {PORT}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n--- Server Stopped by User ---")
        sys.exit(0)
