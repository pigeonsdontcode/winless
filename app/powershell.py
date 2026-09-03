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
        print(process.stderr)
        raise Exception("its not the wrapper this time!")

    return process.stdout

def handle_tasks(tasks, path):
    for option in tasks:
        name, script = option[0]
        print(f"runtime path: {path / script}")
        print(f"\nfeature name: {name}\nscript name: {script}")
        print("running:")
        for feature in option[1]:
            func, msg = feature
            print(f"   function: {func}\n   message: {msg}")
            run(path, script, func)