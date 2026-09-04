import pathlib
from blessed import Terminal

from app.menu import (
    Selection,
    clr
)
from app.data import collect_options
from app.ui import (
    run_selection,
    run_tasks
)

def main() -> None:
    term = Terminal()
    sel = Selection()
    options = collect_options()

    global tasks; tasks = []

    run_selection(
        term,
        sel,
        options,
        tasks
    )

    path = pathlib.Path.cwd() / "scripts"

    output = run_tasks(
        term,
        tasks,
        path
    )

    # grammar function
    # repeating the statement inline in every string is hardly readable
    def g(arr) -> str:
        return '' if arr == 1 else 's'

    # successful count
    suc = output[0] - output[1]

    print(f"\nRan {clr.green if suc > 0 else clr.gray}{suc}{clr.r} successful task{g(suc)}")
    print(f"{clr.red if output[1] > 0 else clr.gray}{output[1]}{clr.r} task{g(output[1])} failed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"write better code:\n{e}")