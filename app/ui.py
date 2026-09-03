from app.menu import fmt
from app.logic import (
    check,
    collect_tasks,
    change_selection
)

def run_tui(
    term,
    sel,
    options,
    tasks
    ) -> None:

    with (
        term.fullscreen(),
        term.cbreak(),
        term.hidden_cursor()
        ):

        # menu logic starts here
        while True:
            print(term.clear, flush=True)

            global i; i = 0

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
                    change_selection('up', sel, i)
                # arrow key down bind,
                # will incremenet selection to move arrow down
                case 'KEY_DOWN':
                    change_selection('down', sel, i)
                # enter key bind,
                # will accent and proceed with the selected functions
                # (and exiting selection menu)
                case 'KEY_ENTER':
                    collect_tasks(options, tasks)
                    break
                # None for now defines space bar, but also binds to other keys
                # due to lib tomfoolery, will likely need a replacement later
                case None:
                    check(options, sel.value)

            # reduce buffer output to prevent screen flickering
            for _ in range(10):
                print(' ', flush=True)