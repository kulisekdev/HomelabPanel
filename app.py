from flask import render_template, redirect, request, Flask, send_from_directory, url_for, make_response   
from Functions.config import get_config, set_config
from Functions.usage import get_system_usage
from Functions.services import start_service, stop_service, enable_service, disable_service, service_status
from Functions.hash import hash_password, verify_hashed_password
from traceback import format_exc
import socket
import secrets

app = Flask(__name__, template_folder="Pages", static_folder="static")


@app.route("/", methods=["GET", "POST"])
def index():
    if verify_hashed_password(get_config("config.toml")["app"]["current_cookie"], request.cookies.get("session")):
        return redirect(url_for("panel_home"))
    config = get_config("config.toml")
    config_app = config["app"]
    print(request.method)
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
                    set_config("config.toml", "app", "current_cookie", hashed_cookie["result"])
                    response = make_response(redirect(url_for("panel_home")))
                    response.set_cookie("session", cookie_value)
                    return response

    return render_template(
        "login.html",
        info={
            "title": config_app["name"],
            "footer": config_app["name"],
            "ip": request.host.split(":")[0],
            "hostname": socket.gethostname()
        })

@app.route("/panel")
def panel_home():
    return render_template("home.html")


@app.route("/panel/setup", methods=["GET","POST"])
def setup_panel():
    config_app = get_config("config.toml")["app"]

    if get_config("config.toml")["app"]["setup"]:
        return render_template("error.html", info={
            "title": config_app["name"],
            "footer": config_app["name"],
            "ip": request.host.split(":")[0],
            "hostname": socket.gethostname(),
            "error": "Error!",
            "error_desc": "Panel already has been set-up. if you'd wish to set up again, toggle setup to false in config."
        })
    if request.method == "POST" and not get_config("config.toml")["app"]["setup"]:
        form = request.form
        password = form.get("passwd")
        print(f"got request: {request.method}")

        if password:

            hashedPass = hash_password(password)
            if hashedPass["success"]:
                set_pass = set_config("config.toml", "app", "panel_password", hashedPass["result"])
                if set_pass["success"]:
                    try:
                        verify_password = verify_hashed_password(get_config("config.toml")["app"]["panel_password"], password)
                        print("hash is valid.")
                        if verify_password:
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
            "footer": config_app["name"],
            "ip": request.host.split(":")[0],
            "hostname": socket.gethostname(),
    })