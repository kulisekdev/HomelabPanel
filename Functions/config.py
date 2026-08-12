import tomllib
import tomli_w
import traceback

def get_config(file: str, section: str) -> dict:
    try: 
        if not isinstance(file, str):
            raise TypeError(f"file must be str, got {type(file).__name__}")
        if not isinstance(section, str):
            raise TypeError(f"section must be str, got {type(section).__name__}")
        
        with open(file, "rb") as f:
            return tomllib.load(f)[section]
    except FileNotFoundError:
        return {"msg": "File not found!", "success": False}
    except KeyError:
        return {"msg": f"Section '{section}' not found!", "success": False}
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
        return {"msg": "Successfully written new config.", "success": True}
    except FileNotFoundError:
        return {"msg": "File not found!", "success": False}
    except KeyError as e:
        return {"msg": f"Section '{e}' not found!", "success": False}
    except PermissionError:
        return {"msg": f"Permissions denied, check file permissions.", "success": False}
    except Exception:
        return {"msg": f"General Exception: {traceback.format_exc()}", "success": False}