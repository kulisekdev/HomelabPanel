import tomllib

def get_config(section: str) -> dict:
    with open("config.toml", "rb") as f:
        return tomllib.load(f)[section]
