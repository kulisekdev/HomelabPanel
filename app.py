import flask
from flask import render_template, redirect, request, Flask
import tomllib
from Functions.config import get_config
from Functions.usage import get_system_usage


app = Flask(__name__, template_folder="Pages")


@app.route("/")
def index():
    return "OK!", 300

@app.get("/system/usage")
def usage_report():
    return get_system_usage()