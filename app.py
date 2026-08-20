from flask import render_template, redirect, request, Flask, send_from_directory, url_for, make_response, jsonify
from flask_socketio import SocketIO
from Functions.config import get_config, set_config
from Functions.usage import get_system_usage, get_ips
from Functions.services import start_service, stop_service, enable_service, disable_service, service_status, add_pinned, remove_pinned
from Functions.hash import hash_password, verify_hashed_password
from Functions.logger import LOG_DIR, logger
from traceback import format_exc
import socket
import secrets
import logging

logger.info("Starting panel...")
app = Flask(__name__, template_folder="Pages", static_folder="static")
sio = SocketIO(app=app)

@app.route("/", methods=["GET", "POST"])
def index():
    config = get_config("config.toml")
    config_app = config["app"]
    if verify_hashed_password(get_config("config.toml")["app"]["current_cookie"], request.cookies.get("session")):
        return redirect(url_for("panel_home"))

    if not config_app["setup"]:
        return redirect(url_for("setup_panel"))

    if request.method == "POST":
        if verify_hashed_password(get_config("config.toml")["app"]["current_cookie"], request.cookies.get("session")):
            return redirect(url_for("panel_home"))
        form = request.form
        password = form.get("passwd")
        if password:
            hashed_result = verify_hashed_password(get_config("config.toml")["app"]["panel_password"], password)
            if hashed_result:
                cookie_value = secrets.token_urlsafe(32)
                hashed_cookie = hash_password(cookie_value)
                if hashed_cookie["success"]:
                    logger.info(f"an user with IP: {request.remote_addr} has logged in.")
                    set_config("config.toml", "app", "current_cookie", hashed_cookie["result"])
                    response = make_response(redirect(url_for("panel_home")))
                    response.set_cookie("session", cookie_value, 600)
                    return response
            else:
                return render_template("login.html", error=True, info={
                    "title": config_app["name"],
                    "footer": config_app["footer"],
                    "ip": get_ips(),
                    "hostname": socket.gethostname()
                })

    
    return render_template(
        "login.html",
        info={
            "title": config_app["name"],
            "footer": config_app["footer"],
            "ip": get_ips(),
            "hostname": socket.gethostname()
        })
@app.route("/panel")
def panel_home():
    if verify_hashed_password(get_config("config.toml")["app"]["current_cookie"], request.cookies.get("session")):
        config_app = get_config("config.toml")["app"]

        return render_template("home.html", info={
            "title": config_app["name"],
            "footer": config_app["footer"],
            "ip": get_ips(),
            "hostname": socket.gethostname(),
        })
    return redirect(url_for("index"))    

@app.route("/panel/setup", methods=["GET","POST"])
def setup_panel():
    config_app = get_config("config.toml")["app"]

    if get_config("config.toml")["app"]["setup"]:
        return render_template("error.html", info={
            "title": config_app["name"],
            "footer": config_app["footer"],
            "ip": get_ips(),
            "hostname": socket.gethostname(),
            "error": "Error!",
            "error_desc": "Panel already has been set-up. if you'd wish to set up again, toggle setup to false in config."
        })
    if request.method == "POST" and not get_config("config.toml")["app"]["setup"]:
        form = request.form
        password = form.get("passwd")
        print(f"got request: {request.method}")

        if password and form.get("port") and form.get("host"):
            hashedPass = hash_password(password)
            if hashedPass["success"]:
                set_pass = set_config("config.toml", "app", "panel_password", hashedPass["result"])
                set_host = set_config("config.toml", "gunicorn", "host", form.get("host"))
                set_port = set_config("config.toml", "gunicorn", "port", form.get("port"))
                if set_pass["success"] and set_host["success"] and set_port["success"]:
                    try:
                        logger.info(f"panel has been setup successfully! IP: {form.get("host")}, PORT: {form.get("port")}")
                        result = set_config(file="config.toml", section="app", name="setup", value=True)
                        print(result)
                        return redirect(url_for("index"))
                    except Exception as e:
                        return {"msg": f"Error: {format_exc()}", "success": False}
                else:
                    return {"msg": f"Verification failed... {set_pass["msg"]}", "success": False}
            else:
                return {"msg": f"Failed to hash the password... {hashedPass["msg"]}", "success": False}
        else:
            return {"msg": f"no password specified.", "success": False}
    return render_template("setup.html", info={
            "title": config_app["name"],
            "footer": config_app["footer"],
            "ip": get_ips(),
            "hostname": socket.gethostname(),
    })

@sio.on("usage_info")
def usage_info():
    return get_system_usage()

@sio.on("service")
def service_manip(data):
    if data["action"] and data["service_name"]:
        action = data["type"]
        service_name = data["service_name"]
        if action == "start":
            start_service(service_name)
        if action == "stop":
            stop_service(service_name)
        if action == "enable":
            enable_service(service_name)
        if action == "disable":
            disable_service(service_name)

@sio.on("get_logs")
def panel_logs():    
    log_file = LOG_DIR / "panel.log"

    if not log_file.exists():
        return jsonify([])

    logs = log_file.read_text(
        encoding="utf-8"
    ).splitlines()[-50:]
    return logs

@sio.on("get_pinned_services")
def pinned_services():
    currently_pinned: list = get_config("config.toml")["user"]["pinned_services"]

    response_list = []

    for service in currently_pinned:
        status = service_status(service)

        list_formula = {
            "name": status["name"],
            "status": True if status["activestate"] == "active" else False
        }
        if status["name"] in response_list:
            continue

        response_list.append(list_formula)

    print(response_list)
    return response_list