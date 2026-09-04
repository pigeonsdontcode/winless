import time
from app.powershell import run
from app.menu import (
    clr,
    fmt,
    title
)
from app.logic import (
    check,
    collect_tasks,
    change_selection
)

def run_selection(
    term,
    sel,
    options,
    tasks
    ) -> None:

    with (
        term.fullscreen(),
        term.cbreak(),
        term.hidden_cursor(),
        term.mouse_enabled(report_motion=True)
        ):

        # menu logic starts here
        while True:
            print(
                term.clear,
                flush=True,
                end=''
            )

            print(title, flush=True)

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
            key = term.inkey()

            match(key.name):
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
                case None | 'MOUSE_LEFT':
                    check(options, sel.value)
                # mouse movement, MOUSE_LEFT speaks for itself,
                # hover over options and click on them to check them
                # will cause screen flickering
                # due to inconsistent buffer output + fast mouse input
                case 'MOUSE_MOTION':
                    # raw mouse y doesn't dynamically align with the options
                    # we'll define the difference in lines between 0 (where the title currently is)
                    # and where the actual options start showing up
                    diff = len(title.splitlines()) + 1
                    y = key.mouse_yx[0]

                    if (0 + diff) <= y < (i + diff):
                        sel.selection = (y + 1) - diff

            # reduce buffer output to prevent screen flickering
            # why does it do that? IDK don't ask me
            for _ in range(18):
                print(' ', flush=True)

def run_tasks(
    term,
    tasks,
    path
    ) -> tuple:

    with (
        term.cbreak(),
        term.hidden_cursor()
        ):

        while True:
            total = 0

            for task in tasks:
                for _ in task[1]:
                    total += 1

            print(f"{total} task{'s' if total != 1 else ''} found", flush=True)

            current = 0
            failed = 0

            for task in tasks:
                name, script = task[0]
                print(f"\nRunning: {name}", flush=True)
                for option in task[1]:
                    current += 1
                    prefix = f" {clr.gray}{current}{clr.r}/{clr.gray}{total}{clr.r} "
                    func, msg = option
                    print(f"{prefix}{msg}", flush=True)

                    try:
                        run(path, script, func)
                    except Exception:
                        failed += 1

                    time.sleep(0.5)

            return (
                total,
                failed
            )