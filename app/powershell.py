import os
import subprocess

def run(path, script, func):
    scriptpath = os.path.join(path, script)

    command = [
        "powershell.exe", "-ExecutionPolicy", "Bypass", "-Command",
        f". '{scriptpath}'; & {func}"
    ]

    process = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if process.stderr:
        raise Exception("its not the wrapper this time!")

    return process.stdout
