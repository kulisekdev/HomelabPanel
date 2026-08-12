import tomllib
import tomli_w
import traceback

def get_config(file: str) -> dict:
    try: 
        if not file.endswith(".toml"):
            raise Exception("file isn't a toml file!")
        if not isinstance(file, str):
            raise TypeError(f"file must be str, got {type(file).__name__}")
        
        with open(file, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return {"msg": "File not found!", "success": False}
    except PermissionError:
        return {"msg": f"Permissions denied, check file permissions.", "success": False}
    except TypeError as e:
        return {"msg": str(e), "success": False} 
    except Exception:
        return {"msg": f"General Exception: {traceback.format_exc()}", "success": False}

def set_config(file: str, section: str, name: str, value):
    # get current config.
    current_config = get_config(file)
    
    # load new entry into the section -> name -> value
    current_config[section][name] = value
    try: 
        with open("config.toml", "wb") as f:
            tomli_w.dump(current_config, f)
        return {"msg": f"Successfully applied new config value for entry '{name}' in section '{section}' in '{file}'", "success": True}
    except FileNotFoundError:
        return {"msg": "File not found!", "success": False}
    except KeyError as e:
        return {"msg": f"Section '{e}' not found!", "success": False}
    except PermissionError:
        return {"msg": f"Permissions denied, check file permissions.", "success": False}
    except Exception:
        return {"msg": f"General Exception: {traceback.format_exc()}", "success": False}