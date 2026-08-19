# Serverpanel

A small Python-based server management panel. The project appears to provide a web interface for configuring and monitoring server services, with setup, home, and error pages.

## Structure

* `app.py` — main web application entry point
* `config.toml` / `Functions/config.py` — configuration handling
* `Functions/services.py` — service management logic
* `Functions/usage.py` — resource/usage information
* `Functions/hash.py` — hashing utilities
* `Functions/errors.py` — application error handling
* `loop.py` — background or recurring application logic
* `Pages/` — HTML templates for the web interface
* `run.sh` — script for starting the application
* `Libraries/` — Python virtual environment and installed dependencies

## Running

The project includes a `run.sh` startup script. It likely initializes the environment and launches `app.py`.

```bash
./run.sh
```

## Status

This appears to be a lightweight server-panel application, likely intended to provide basic server/service administration through a browser.
