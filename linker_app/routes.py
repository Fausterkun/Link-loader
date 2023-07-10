# from flask import render_template, request, g, redirect, url_for
from flask import render_template

from linker_app import bp, socketio, log_buffer  # app
from . import app


@bp.route("/")
@bp.route("/index")
def hello_world():  # put application's code here
    app.logger.warning("User visit index page")
    # return render_template(os.path.join(BASE_PATH, 'templates', 'index.html'))
    return render_template("index.html")


@bp.route("/links", methods=["GET", "POST"])
def links():
    app.logger.info("User visit links page")
    return "<h1>hi max</h1>"


@bp.route("/logs", methods=["GET"])
def logs():
    app.logger.info("User visit logs page")
    return render_template("logs.html")


@bp.route("/test_logs", methods=["GET"])
def test_logs():
    # app.logger.exception("EXCEPTION")
    app.logger.critical("critical")
    app.logger.warning("warning")
    app.logger.debug("debug")
    app.logger.info("info")
    return "<h1>Test log messages for all levels called. Check web log viewer</h1>"


# ------------- Websocket dynamic log notifications ------------------


@socketio.on("connect", namespace="/logs")
def connect():
    # app.logger.info("Websocket connection to /logs page")
    logs = log_buffer
    socketio.emit(event="init_logs", data={"logs": logs}, namespace="/logs")
    # TODO: send previous log messages
    # socketio.emit("new_log",  namespace="/logs")

    # @socketio.on("new_log", namespace="/logs")
    # def send_log(lines: list[str]):
    #     # print("user connected")
    #     # logs = ["some line 1", "some line 2"]
    #     # socketio.emit("new_log", {"logs": logs}, namespace="/logs")
    #     # socketio.call("new_log", data={"logs": logs}, namespace="/logs")
