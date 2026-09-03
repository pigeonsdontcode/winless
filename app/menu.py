from builtins import print as _p
from app.logic import changeselection, check, collectplanned

# rewrite print functions to enable flush by default
# to reduce output buffering and minimize tui flickering
def print(*args, **kwargs):
    kwargs.setdefault("flush", True)
    _p(*args, **kwargs)

class pfx:
    global spacing, uiprefix
    spacing = ' '*3
    uiprefix = '|'

    class parent:
        pre = uiprefix + spacing

        # use formatted strings to add colors later
        base = f'{pre} [ ] '
        base_hover = f'{pre}>[ ] '
        checked = f'{pre} [X] '
        checked_hover = f'{pre}>[X] '

    class child:
        pre = uiprefix + (spacing * 2)

        base = f'{pre} [ ] '
        base_hover = f'{pre}>[ ] '
        checked = f'{pre} [X] '
        checked_hover = f'{pre}>[X] '

class Selection:
    def __init__(self) -> None:
        self.default = 1
        self.selection = self.default

    # just incase we might use int method (probably not)
    def __int__(self):
        return self.selection

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
    content: str,
    # require selection, checked & parent states
    selected: bool,
    checked: bool,
    parent: bool = False
    ) -> str:

    p = pfx.parent if parent else pfx.child

    pfxmap = {
        (False, False): p.base,
        (True, False): p.base_hover,
        (False, True): p.checked,
        (True, True): p.checked_hover,
    }

    return pfxmap[(selected, checked)] + content

def handlekey(
        key,
        selection: Selection,
        increment: int,
        arr: list,
        planned: list
        ) -> None:
    # possible menu keybinds
    binds = {
        # arrow key up bind,
        # will decrement eventual selection to move the arrow up
        'KEY_UP': lambda: changeselection('up', selection, increment),
        # arrow key down bind,
        # will incremenet selection to move arrow down
        'KEY_DOWN': lambda: changeselection('down', selection, increment),
        # enter key bind,
        # will accent and proceed with the selected functions
        # (and exiting selection menu)
        'KEY_ENTER': lambda: collectplanned(arr, planned),
        # None for now defines space bar, but also binds to other keys
        # due to lib tomfoolery, will likely need a replacement later
        None: lambda: check(arr, selection.value)
    }


    action = binds.get(key)
    # linter error wants me to handle None (the dict can't return None)
    if action != None:
        action()