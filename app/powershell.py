import os
import subprocess

def exclude(err):
    exclusionlist = [
        # there will always be temp files in use that can't be deleted
        # we do this to prevent every file from raising errors
        "RemoveFileSystemItemIOError",
        # empty bin will result in an error
        "FailedToClearRecycleBin",
    ]

    for exc in exclusionlist:
        if exc in err:
            return True

    return False

def run(path, script, func, uac: bool = False):
    scriptpath = os.path.join(path, script)

    args = [
        "powershell.exe", "-ExecutionPolicy", "Bypass", "-Command",
    ]

    if uac:
        args.extend(["-verb", "RunAs"])

    command = f". '{scriptpath}'; & {func}"

    args.append(command)

    process = subprocess.run(
        args,
        capture_output=True,
        text=True
    )

    # whole process error handling should be improved in the future
    if process.stderr:
        # if already ran with admin, raise final exception for this process
        if uac:
            raise Exception("its not the wrapper this time!")

        # if error, try running as admin
        try:
            run(path, script, func, True)
        except Exception:
            if exclude(process.stderr):
                return

            # only for debug purposes
            print(process.stderr)
            raise Exception("its not the wrapper this time!")


    # powershell output isn't used, might need to be removed later
    return process.stdout