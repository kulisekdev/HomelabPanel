import flask
from flask import render_template, redirect, request, Flask
import tomllib
from Functions.config import get_config, set_config
from Functions.usage import get_system_usage
from Functions.services import start_service, stop_service, enable_service, disable_service, service_status


app = Flask(__name__, template_folder="Pages")


@app.route("/")
def index():
    return "OK!", 300

@app.get("/system/usage")
def usage_report():
    return get_system_usage()

@app.get("/system/config")
def get_configuration():
    return get_config(2232, "app")

@app.get("/system/testedit")
def test_edit():
    return set_config(file="config", section="app", name="test", value="Yessir!")

@app.get("/system/start")
def start_service_file():
    return start_service("testservice.service")

@app.get("/system/stop")
def stop_service_file():
    return stop_service("testservice.service")

@app.get("/system/enable")
def enable_service_file():
    return enable_service("testservice.service")

@app.get("/system/disable")
def disable_service_file():
    return disable_service("testservice.service")

@app.get("/system/info")
def get_service_info():
    return service_status("testservice.service")