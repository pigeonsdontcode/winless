import pathlib
from blessed import Terminal

from app.menu import Selection
from app.data import collect_options
from app.ui import run_tui
from app.powershell import handle_tasks

def main() -> None:
    term = Terminal()
    sel = Selection()
    options = collect_options()

    global tasks; tasks = []

    # abstract main.py as much as possible!!!
    run_tui(
        term,
        sel,
        options,
        tasks
    )

    path = pathlib.Path.cwd() / "scripts"

    print(path)

    print("run!")
    print(tasks)

    handle_tasks(tasks, path)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"write better code:\n{e}")