#!/bin/bash
# testing for now.
cd /home/luke/Plocha/Serverpanel/

host=$(python -c 'import tomllib; print(tomllib.load(open("config.toml", "rb"))["gunicorn"]["host"])')
port=$(python -c 'import tomllib; print(tomllib.load(open("config.toml", "rb"))["gunicorn"]["port"])')

CONNECTION="$host:$port"

/home/luke/Plocha/Serverpanel/Libraries/bin/gunicorn --worker-class gevent app:app --bind $CONNECTION --workers 1