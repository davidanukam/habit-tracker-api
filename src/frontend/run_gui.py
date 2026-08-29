import sys
from pathlib import Path
from streamlit.web import cli as stcli


def main():
    gui_path = Path(__file__).parent / "gui.py"
    sys.argv = ["streamlit", "run", str(gui_path)]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
