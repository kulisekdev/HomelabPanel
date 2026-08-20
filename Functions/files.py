import subprocess
import os

def delete(args, path):
    try:
        subprocess.run(["rm", args, path])
    except Exception as e:
        return {
            "success": False,
            "msg": f"error: {e}"
        }

def create(path: str, name):
    if not path.endswith("/"):
        path = path + "/" + name
    path = path + name
    try:
        subprocess.run(["touch", f"{path}"])
        return {"success": True}
    except Exception as e:
        return {"success": False, "msg": f"error: {e}"}
