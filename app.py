import flask
from flask import render_template, redirect, request, Flask
import tomllib
from Functions.config import get_config, set_config
from Functions.usage import get_system_usage


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
    return set_config(file="config.toml", section="app", name="test", value="Yessir!")