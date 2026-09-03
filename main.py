from blessed import Terminal
from app.data import fetchoptions
from app.menu import (
    Selection,
    fmt,
    handlekey
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

            # key input handling later
            key = term.inkey()
            handlekey(key.name, sel, i, options, planned)

            # reduce buffer output to prevent screen flickering
            for _ in range(10):
                print(' ', flush=True)

    print("run!")
    print(planned)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"write better code:\n{e}")