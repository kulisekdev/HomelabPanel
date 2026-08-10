import flask
from flask import render_template, redirect, request, Flask
import tomllib
from Functions.config import load_config



app = Flask(__name__, template_folder="Pages")


@app.route("/")
def index():
    return "OK!", 300


if __name__ == "__main__": 
    app.run(host="127.0.0.1", port=1111)