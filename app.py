import flask
from flask import render_template, redirect, request, Flask
import tomllib
from Functions.config import get_config



app = Flask(__name__, template_folder="Pages")


@app.route("/")
def index():
    return "OK!", 300

