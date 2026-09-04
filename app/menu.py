from colorama import (
    Fore as f,
    Style as s,
    init
)

init(autoreset=True)

class clr:
    r = f.RESET

    bright = s.BRIGHT
    dim = s.DIM

    lightblue = f.CYAN
    blue = f.LIGHTBLUE_EX
    white = f.WHITE
    yellow = f.LIGHTYELLOW_EX
    gray = f.LIGHTBLACK_EX
    red = f.LIGHTRED_EX
    green = f.LIGHTGREEN_EX

class pfx:
    class box:
        def __init__(self, indent: str = '') -> None:
            self.indent = indent

            self.base = f'{indent}  [ ] '
            self.base_hover = f'{indent}{clr.blue}> [ ] '
            self.checked = f'{indent}  [{clr.lightblue}X{clr.r}] '
            self.checked_hover = f'{indent}{clr.blue}> [X] '

    parent = box()
    child = box(' ' * 3)

class Selection:
    def __init__(self) -> None:
        self.default = 1
        self.selection = self.default

    @property
    def value(self) -> int:
        return self.selection

    @property
    def increment(self) -> None:
        self.selection += 1

    @property
    def decrement(self) -> None:
        self.selection -= 1

def fmt(
    msg: str,
    # require selection, checked & parent states
    selected: bool,
    checked: bool,
    parent: bool = False
    ) -> str:

    p = pfx.parent if parent else pfx.child

    # ( is item selected?, is item checked?)
    pfxmap = {
        (False, False): p.base,
        (True, False): p.base_hover,
        (False, True): p.checked,
        (True, True): p.checked_hover,
    }

    if not selected:
        msg = (clr.white if parent else clr.gray) + msg

    return pfxmap[(selected, checked)] + msg

s = ' ' * 2
title = \
f"""
{s}╭─ {clr.lightblue}Winless{clr.r} ──────────────────────────────────────────────╮
{s}│ Small utility tweak menu for Windows                   │
{s}│ {clr.gray}                                                     {clr.r}  │
{s}│ {clr.gray}Navigate the selection menu with the arrow keys (↑ ↓)  {clr.r}│
{s}│ {clr.gray}or hover over them with your mouse                   {clr.r}  │
{s}│ {clr.gray}Select the checkboxes with SPACE or left mouse click {clr.r}  │
{s}│ {clr.gray}Press 'ENTER' to apply the selected options {clr.r}           │
{s}╰────────────────────────────────────────────────────────╯
"""