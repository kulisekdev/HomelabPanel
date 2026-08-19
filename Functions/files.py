import subprocess

def delete(args, path):
    subprocess.run(["rm", args, path])

def create(path: str, name):
    if not path.endswith("/"):
        path = path + "/" + name
    path = path + name
    subprocess.run(["touch", f"{path}"])

