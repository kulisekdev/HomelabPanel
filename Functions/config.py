import tomllib
import tomli_w
import traceback
from Functions.logger import logger
def get_config(file: str) -> dict:
    try: 
        if not file.endswith(".toml"):
            raise Exception("file isn't a toml file!")
        if not isinstance(file, str):
            raise TypeError(f"file must be str, got {type(file).__name__}")
        
        with open(file, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        logger.error(f"Functions/config.py/get_config: FileNotFoundError: {e}")
        return {"msg": "File not found!", "success": False}
    except PermissionError:
        logger.error(f"Functions/config.py/get_config: PermissionError: {e}")
        return {"msg": f"Permissions denied, check file permissions.", "success": False}
    except TypeError as e:
        logger.error(f"Functions/config.py/get_config: TypeError: {e}")
        return {"msg": str(e), "success": False} 
    except Exception:
        logger.error(f"Functions/config.py/get_config: Exception: {e}")
        return {"msg": f"General Exception: {traceback.format_exc()}", "success": False}

def set_config(file: str, section: str, name: str, value):
    if not file.endswith(".toml"):
        return {"msg": "file isn't a toml file!", "success": False}
    # get current config.
    current_config = get_config(file)
    
    # load new entry into the section -> name -> value
    current_config[section][name] = value
    try: 
        
        with open("config.toml", "wb") as f:
            tomli_w.dump(current_config, f)
        logger.info(f"Functions/config.py/set_config: Successfully applied new config value for entry '{name}' in section '{section}' in '{file}' with '{value}'")
        return {"msg": f"Functions/config.py: Successfully applied new config value for entry '{name}' in section '{section}' in '{file}' with '{value}'", "success": True}
    except FileNotFoundError as e:
        logger.error(f"Functions/config.py/set_config: FileNotFoundError: {e}")
        return {"msg": "File not found!", "success": False}
    except KeyError as e:
        logger.error(f"Functions/config.py/set_config: KeyError: {e} ")
        return {"msg": f"Section '{e}' not found!", "success": False}
    except PermissionError as e:
        logger.error(f"Functions/config.py/set_config: PermissionError: {e}")
        return {"msg": f"Permissions denied, check file permissions.", "success": False}
    except Exception as e:
        logger.error(f"Functions/config.py/set_config: Exception: {e}  ")
        return {"msg": f"Exception: {traceback.format_exc()}", "success": False}