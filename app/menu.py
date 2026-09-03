from builtins import print as _p

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
        base = f'{pre}[ ] '
        base_hover = f'{pre}>[ ] '
        checked = f'{pre}[X] '
        checked_hover = f'{pre}>[X] '

    class child:
        pre = uiprefix + (spacing * 2)

        base = f'{pre}[ ] '
        base_hover = f'{pre}>[ ] '
        checked = f'{pre}[X] '
        checked_hover = f'{pre}>[X] '

class Selection:
    def __init__(self) -> None:
        self.selection = 0

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