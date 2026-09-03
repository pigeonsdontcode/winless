def changeselection(direction: str, selection, increment: int):
    match(direction):
        case 'up':
            if selection.value > selection.default:
                selection.decrement
        case 'down':
            if selection.value < increment:
                selection.increment

def findidx(arr: list, idx: int):
    i = 0
    def parse(parent):
        nonlocal i

        if not isinstance(parent, list):
            return

        for child in parent:
            i += 1
            if i == idx:
                return child

            # child conditions:
            #   is array
            #   has more than 1 grandchild (first grandchild should be non-displayed option name)
            #   2nd grandchild is an array
            if (
                isinstance(child, list),
                len(child) > 1,
                isinstance(child[1], list)
                ):

                grandchildren = child[1][2] if len(child[1]) > 2 else []

                # parse callback when more subarrays are found,
                # cba to hardcode the 5th dimension
                nextgen = parse(grandchildren)

                # return nextgen if nextgen else None
                if nextgen:
                    return nextgen

        return

    return parse(arr)

def check(arr, selection):
    item = findidx(arr, selection) or []
    try:
        item[2] = not item[2]
    # we use IndexError to asume that if item[2] does not exist,
    # then it is a child element
    except IndexError:
        item[1][3] = not item[1][3]

# reminder: document option positions later!!!!!!
def collectplanned(arr, planned):
    for parent in arr:
        arr = []
        arr.append([
                parent[1][0],
                parent[1][1]
                ])

        between = []

        for child in parent[1][2]:
            if child[2] or parent[1][3]:
                between.append([
                        child[1][2],
                        child[1][1]
                        ])

            arr.append(between)
        if len(arr[1]) == 0:
            continue

        planned.append(arr)

    print(planned)
    __import__('time').sleep(5)