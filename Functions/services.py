from pystemd.systemd1 import Unit, manager
from Functions.errors import FileFormatError, ServiceError
from traceback import format_exc
from datetime import datetime, timezone
from Functions.config import set_config, get_config
from Functions.logger import logger
import os
from pathlib import Path


def start_service(name: str) -> dict:
    try:
        if not isinstance(name, str):
            raise TypeError(f"name should be str, got {type(name).__name__}")

        if not name.endswith(".service"):
            raise FileFormatError(f"Invalid file format error, expected .service, got '{name}'")
        
        with Unit(name.encode()) as unit:
            if unit.Unit.LoadState == b"bad-setting":
                raise ServiceError(f"{name} has a bad setting! check syntax.")
            if unit.Unit.LoadState == b"not-found":
                raise ServiceError(f"{name} was not found!")
            
            if unit.Unit.LoadState == b"masked":
                raise ServiceError(f"{name} is masked!")
            
            if unit.Unit.ActiveState == b"activating" and unit.Unit.SubState == b"auto-restart":
                raise ServiceError(f"{name} failed to start and systemd is trying to start it indefinitely. consider restarting.")

            if unit.Unit.ActiveState == b"active":
                raise ServiceError(f"{name} is already active!")
            
            if unit.Unit.ActiveState == b"inactive":
                unit.Unit.Start(b"replace")
            


            
            logger.info(f"Functions/services.py/enable_service: {name} has been activated.")
            return {"msg": f"'{name} started successfully!", "success": True}
    except ServiceError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except TypeError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except FileFormatError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except Exception:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }

def stop_service(name: str) -> dict:
    try:
        if not isinstance(name, str):
            raise TypeError(f"name should be str, got {type(name).__name__}")

        if not name.endswith(".service"):
            raise FileFormatError(f"Invalid file format error, expected .service, got '{name}'")
        
        with Unit(name.encode()) as unit:
            print(unit.Unit.ActiveState)
            if unit.Unit.LoadState == b"bad-setting":
                raise ServiceError(f"{name} has a bad setting! check syntax.")
            
            if unit.Unit.LoadState == b"not-found":
                raise ServiceError(f"{name} was not found!")
            
            if unit.Unit.LoadState == b"masked":
                raise ServiceError(f"{name} is masked!")
            
            if unit.Unit.ActiveState == b"activating" and unit.Unit.SubState == b"auto-restart":
                raise ServiceError(f"{name} failed to start and systemd is trying to start it indefinitely. consider restarting.")

            if unit.Unit.ActiveState == b"inactive":
                raise ServiceError(f"{name} is already inactive!")
            
            if unit.Unit.ActiveState == b"active":
                unit.Unit.Stop(b"replace")
            logger.info(f"Functions/services.py/enable_service: {name} has been stopped.")
            return {"msg": f"'{name} stopped successfully!", "success": True}
        
    except ServiceError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except TypeError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except FileFormatError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except Exception:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }

def enable_service(name: str) -> dict:


    try:
        
        if not isinstance(name, str):
            raise TypeError(f"name should be str, got {type(name).__name__}")

        if not name.endswith(".service"):
            raise FileFormatError(f"Invalid file format error, expected .service, got '{name}'")
        
        with Unit(name.encode()) as unit:
            if unit.Unit.LoadState == b"bad-setting":
                raise ServiceError(f"{name} has a bad setting! check syntax.")
            
            if unit.Unit.LoadState == b"not-found":
                raise ServiceError(f"{name} was not found!")

            state = manager.Manager.GetUnitFileState(name.encode())
            if state == b"enabled":
                raise ServiceError(f"{name} is already enabled!")

            if state == b"disabled":
                manager.Manager.EnableUnitFiles([name.encode()], False, False)
            logger.info(f"Functions/services.py/enable_service: {name} has been enabled.")

            return {"msg": f"'{name} enabled successfully!", "success": True}
        
    except ServiceError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except TypeError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except FileFormatError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except Exception:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }

def disable_service(name: str) -> dict:
    try:
        
        if not isinstance(name, str):
            raise TypeError(f"name should be str, got {type(name).__name__}")

        if not name.endswith(".service"):
            raise FileFormatError(f"Invalid file format error, expected .service, got '{name}'")
        
        with Unit(name.encode()) as unit:
            print(unit.Unit.ActiveState)
            if unit.Unit.LoadState == b"bad-setting":
                raise ServiceError(f"{name} has a bad setting! check syntax.")
            
            if unit.Unit.LoadState == b"not-found":
                raise ServiceError(f"{name} was not found!")

            state = manager.Manager.GetUnitFileState(name.encode())
            if state == b"disabled":
                raise ServiceError(f"{name} is already disabled!")

            if state == b"enabled":
                manager.Manager.DisableUnitFiles([name.encode()], False)
            logger.info(f"Functions/services.py/enable_service: {name} has been disabled.")
            return {"msg": f"'{name} enabled successfully!", "success": True}
        
    except ServiceError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except TypeError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except FileFormatError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except Exception:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }

def restart_service(name: str) -> dict:
    try:
        if not isinstance(name, str):
            raise TypeError(f"name should be str, got {type(name).__name__}")

        if not name.endswith(".service"):
            raise FileFormatError(f"Invalid file format error, expected .service, got '{name}'")
        
        with Unit(name.encode()) as unit:
            print(unit.Unit.ActiveState)
            if unit.Unit.LoadState == b"bad-setting":
                raise ServiceError(f"{name} has a bad setting! check syntax.")
            
            if unit.Unit.LoadState == b"not-found":
                raise ServiceError(f"{name} was not found!")
            

            unit.Unit.Restart(b"replace")
            logger.info(f"Functions/services.py/enable_service: {name} has been restarted.")
            return {"msg": f"'{name} restarted successfully!", "success": True}
    except ServiceError as e:
        return {
            "msg": f"Error: {e}",
            "success": False
        }
    except TypeError as e:
        return {
            "msg": f"Error: {e}",
            "success": False
        }
    except FileFormatError as e:
        return {
            "msg": f"Error: {e}",
            "success": False
        }
    except Exception as e:
        return {
            "msg": f"Error: {e}",
            "success": False
        }

def service_status(name: str) -> dict:
    try:
        if not isinstance(name, str):
            raise TypeError(f"name should be str, got {type(name).__name__}")

        if not name.endswith(".service"):
            raise FileFormatError(f"Invalid file format error, expected .service, got '{name}'")

        with Unit(name.encode()) as unit:
            if unit.Unit.LoadState == b"bad-setting":
                raise ServiceError(f"{name} has a bad setting! check syntax.")
            if unit.Unit.LoadState == b"not-found":
                raise ServiceError(f"{name} was not found!")
            
            if unit.Unit.LoadState == b"masked":
                raise ServiceError(f"{name} is masked!")
            
            timestampEnterActiveState = datetime.fromtimestamp(
                unit.Unit.ActiveEnterTimestamp / 1_000_000, # always gives Thu, 01 Jan 1970 00:00:00 GMT
                tz=timezone.utc
            )
            timestampExitActiveState = datetime.fromtimestamp(
                unit.Unit.ActiveExitTimestamp / 1_000_000, # always gives Thu, 01 Jan 1970 00:00:00 GMT
                tz=timezone.utc
            )

            serviceinfo = {
                "name": name,
                "loadstate": unit.Unit.LoadState.decode(),
                "activestate": unit.Unit.ActiveState.decode(),
                "description": unit.Unit.Description.decode(),
                "substate": unit.Unit.SubState.decode(),
                "started_at": str(timestampEnterActiveState),
                "stopped_at": str(timestampExitActiveState),
            }
            
            return serviceinfo
            
    except ServiceError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except TypeError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except FileFormatError:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }
    except Exception:
        return {
            "msg": f"Error: {format_exc()}",
            "success": False
        }

def list_services() -> list:
    finalservicedir = []

    for path in Path("/etc/systemd/system/").iterdir():
        if path.is_file() and path.suffix== ".service":
            finalservicedir.append(path.name)

    return finalservicedir


def add_pinned(name: str):
    if not name:
        return {"success": False, "msg": "Expected str for name, got None"}
    name = str(name)
    currently_pinned: list = get_config("config.toml")["user"]["pinned_services"]

    if name not in currently_pinned:
        currently_pinned.append(name)
        set_config(file="config.toml", section="user", name="pinned_services", value=currently_pinned)
        logger.info(f"Functions/services.py/enable_service: {name} has been pinned.")
        return {"success": True}
    else:
        return {"success": False, "msg": f"'{name}' is already pinned."}

def remove_pinned(name: str):
    if not name:
        return {"success": False, "msg": "Expected str for name, got None"}
    name = str(name)
    currently_pinned: list = get_config("config.toml")["user"]["pinned_services"]

    if name not in currently_pinned:
        return {"success": False, "msg": f"'{name}' is not in pinned services."}
    if name in currently_pinned:
        logger.info(f"Functions/services.py/enable_service: {name} has been unpinned.")
        currently_pinned.remove(name)
        set_config("config.toml", "user", "pinned_services", currently_pinned)
        return {"success": True}
    else:
        return {"success": False, "msg": f"'{name}' is already pinned."}
