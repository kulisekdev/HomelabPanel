import pystemd.systemd1
from pystemd.systemd1 import Unit, Manager
from Functions.errors import FileFormatError, ServiceError
from traceback import format_exc
from datetime import datetime, timezone
manager = Manager()
manager.load()

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
                "started_at": timestampEnterActiveState,
                "stopped_at": timestampExitActiveState,
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