from blessed import Terminal
from app.data import readoptions
from app.menu import pfx, Selection

def main() -> None:
    term = Terminal()

    with \
        (
            term.fullscreen(),
            term.cbreak(),
            term.hidden_cursor()
        ):

        # menu logic starts here
        while True:
            print(term.clear)

            test = [
                i for i in range(10)
            ]

            for num in test:
                print(num, flush=True)

            # key input handling later
            key = term.inkey()

            # force buffer update to prevent screen flickering
            for _ in range(10):
                print(' ', flush=True)
                # print(' ', end='', flush=True)


    print(readoptions())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"write better code:\n{e}")