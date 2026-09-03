import pathlib
from blessed import Terminal
from app.data import fetchoptions
from app.powershell import handleplanned
from app.menu import (
    Selection,
    fmt,
)
from app.logic import (
    check,
    collectplanned,
    changeselection
)

def main() -> None:
    term = Terminal()

    sel = Selection()
    options = fetchoptions()

    global planned
    planned = []

    with (
        term.fullscreen(),
        term.cbreak(),
        term.hidden_cursor()
        ):

        # menu logic starts here
        while True:
            print(term.clear)

            global i
            i = 0

            for parent in options:
                i += 1

                print(
                    fmt(
                        parent[1][0],
                        sel.value == i,
                        parent[1][3],
                        True
                    ),
                    flush=True
                )

                for child in parent[1][2]:
                    i += 1
                    print(
                        fmt(
                            child[1][0],
                            sel.value == i,
                            child[2] or parent[1][3]
                        ),
                        flush=True
                    )

            # key handling
            match(term.inkey().name):
                # arrow key up bind,
                # will decrement eventual selection to move the arrow up
                case 'KEY_UP':
                    changeselection('up', sel, i)
                # arrow key down bind,
                # will incremenet selection to move arrow down
                case 'KEY_DOWN':
                    changeselection('down', sel, i)
                # enter key bind,
                # will accent and proceed with the selected functions
                # (and exiting selection menu)
                case 'KEY_ENTER':
                    collectplanned(options, planned)
                    break
                # None for now defines space bar, but also binds to other keys
                # due to lib tomfoolery, will likely need a replacement later
                case None:
                    check(options, sel.value)

            # reduce buffer output to prevent screen flickering
            for _ in range(10):
                print(' ', flush=True)

    path = pathlib.Path.cwd() / "scripts"

    print(path)

    print("run!")
    print(planned)

    handleplanned(planned, path)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"write better code:\n{e}")