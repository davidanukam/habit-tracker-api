import os
import sys
import subprocess
from honcho.command import main as honcho_main


def main():
    # If no subcommand was passed (e.g. running via `uv run dev`), default to `start`
    if len(sys.argv) == 1:
        sys.argv.append("start")

    try:
        honcho_main()
    except (KeyboardInterrupt, SystemExit, Exception):
        # Forcefully cleanup child process trees on Windows so Ctrl+C returns to terminal
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(os.getpid())],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        sys.exit(0)


if __name__ == "__main__":
    main()
