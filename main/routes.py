# from flask import render_template, request, g, redirect, url_for
from flask import render_template, request

from main import bp, socketio  # app
from . import app


@bp.route("/")
@bp.route("/index")
def hello_world():  # put application's code here
    app.logger.warning("Visit index ")
    # return render_template(os.path.join(BASE_PATH, 'templates', 'index.html'))
    return render_template("index.html")


@bp.route("/links", methods=["GET", "POST"])
def links():
    app.logger.debug("Visit links")
    return "ok"


@bp.route("/logs", methods=["GET"])
def logs():
    app.logger.info("Visit logs")
    return render_template("logs.html")


# ------------- Websocket dynamic log notifications ------------------


@socketio.on("connect", namespace="/logs")
def connect():
    app.logger.info("Websocket connection to /logs page")
    # socketio.emit("new_log",  namespace="/logs")


# @socketio.on("new_log", namespace="/logs")
# def send_log(lines: list[str]):
#     # print("user connected")
#     # logs = ["some line 1", "some line 2"]
#     # socketio.emit("new_log", {"logs": logs}, namespace="/logs")
#     # socketio.call("new_log", data={"logs": logs}, namespace="/logs")
