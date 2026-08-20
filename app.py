from flask import render_template, redirect, request, Flask, send_from_directory, url_for, make_response, jsonify
from flask_socketio import SocketIO
from Functions.config import get_config, set_config
from Functions.usage import get_system_usage, get_ips
from Functions.services import restart_service,list_services,start_service, stop_service, enable_service, disable_service, service_status, add_pinned, remove_pinned
from Functions.hash import hash_password, verify_hashed_password
from Functions.logger import LOG_DIR, logger
from traceback import format_exc
import socket
from datetime import datetime
import secrets
import logging

logger.info("app.py: Starting panel...")
app = Flask(__name__, template_folder="Pages", static_folder="static")
sio = SocketIO(app=app)

def error_page(error_desc):
    config_app = get_config("config.toml")["app"]

    return render_template("error.html", info={
        "title": config_app["name"],
        "footer": config_app["footer"],
        "ip": get_ips(),
        "hostname": socket.gethostname(),
        "error": "Error!",
        "error_desc": error_desc
    })
def service_page():
    config = get_config("config.toml")
    config_app = config["app"]
    return render_template("services.html",info={
        "title": config_app["name"],
        "footer": config_app["footer"],
        "ip": get_ips(),
        "hostname": socket.gethostname()
    })

def login_page():
    config = get_config("config.toml")
    config_app = config["app"]
    return render_template("login.html", info={
        "title": config_app["name"],
        "footer": config_app["footer"],
        "ip": get_ips(),
        "hostname": socket.gethostname()
    })

def home_page():
    config = get_config("config.toml")
    config_app = config["app"]
    return render_template("home.html", info={
        "title": config_app["name"],
        "footer": config_app["footer"],
        "ip": get_ips(),
        "hostname": socket.gethostname(),
    })
def setup_page():
    config = get_config("config.toml")
    config_app = config["app"]
    return render_template("setup.html", info={
            "title": config_app["name"],
            "footer": config_app["footer"],
            "ip": get_ips(),
            "hostname": socket.gethostname(),
    })

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
                    logger.info(f"app.py/index: an user with IP: {request.remote_addr} has logged in.")
                    set_config("config.toml", "app", "current_cookie", hashed_cookie["result"])
                    response = make_response(redirect(url_for("panel_home")))
                    response.set_cookie("session", cookie_value, 600)
                    return response
            else:
                return login_page()
    return login_page()
@app.route("/panel")
def panel_home():
    if verify_hashed_password(get_config("config.toml")["app"]["current_cookie"], request.cookies.get("session")):
        config_app = get_config("config.toml")["app"]
        logger.info(f"app.py/panel_home: {request.remote_addr} accessed the panel's dashboard.")
        return home_page()
    return redirect(url_for("index"))    

@app.route("/panel/setup", methods=["GET","POST"])
def setup_panel():
    config_app = get_config("config.toml")["app"]

    if get_config("config.toml")["app"]["setup"]:
        return error_page("Panel already has been set-up. if you'd wish to set up again, toggle setup to false in config.toml.")
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
                        logger.info(f"app.py/setup_panel: panel has been setup successfully! Panel config: IP: {form.get("host")}, PORT: {form.get("port")}")
                        set_config(file="config.toml", section="app", name="setup", value=True)
                        return redirect(url_for("index"))
                    except Exception as e:
                        logger.error(f"app.py/setup_panel: an error has occured. {e}")
                        return {"msg": f"Error: {format_exc()}", "success": False}
                else:
                    logger.info(f"app.py/setup_panel: {request.remote_addr} has attempted to log in but failed.")
                    return error_page("some configurations failed to get applied. failed: ")
            else:
                logger.error("app.py/setup_panel: password hashing was unsuccessfull... endpoint: /panel/setup")
                return error_page(f"Failed to hash the password... {hashedPass["msg"]}, report this issue on my discord")
        else:
            return error_page("expected string, got None.")
        
    return setup_page()

@sio.on("usage_info")
def usage_info():
    return get_system_usage()

@sio.on("service")
def service_manip(data):
    print(data)
    if data["action"] == "list":
        return list_services()
    
    if data["action"] and data["name"]:
        print("got action and data.")
        action = data["action"]
        service_name = data["name"]
        if action == "restart":
            return restart_service(service_name)
        if action == "start":
            return start_service(service_name)
        if action == "stop":
            return stop_service(service_name)
        if action == "enable":
            return enable_service(service_name)
        if action == "disable":
            return disable_service(service_name)
        if action == "status":
            return service_status(service_name)
        if action == "pin":
            return add_pinned(service_name)
        if action == "unpin":
            return remove_pinned(service_name)
        if action == "pin_status":
            pinned_list: list = get_config("config.toml")["user"]["pinned_services"]
            if data["name"] in pinned_list:
                return True
            else:
                return False

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

    return response_list

@sio.on("get_time")
def system_time():
    return str(datetime.now().strftime("%Y-%m-%d @ %H:%M:%S"))

@app.route("/panel/services", methods=["GET", "POST"])
def panel_services():
    return service_page()