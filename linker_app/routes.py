# from flask import render_template, request, g, redirect, url_for
from flask import render_template, request
from flask_socketio import join_room, leave_room

from linker_app import bp, socketio, log_buffer  # app
from . import app
from . import counter


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
    # app.logger.info("User visit logs page")
    global counter
    app.logger.info(str(counter))
    counter += 1
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
    room = "room1"
    # join_room(room)
    logs = log_buffer.get_all()
    if not getattr(request, "sid"):
        app.logger.warning(
            'Try ws "connect" event without sid param at request. May be some parser.'
        )
    socketio.emit(
        event="init_logs",
        to=getattr(request, "sid", None),
        data={"logs": logs},
        namespace="/logs",
    )
    # TODO: send previous log messages
    # socketio.emit("new_log",  namespace="/logs")

    # @socketio.on("new_log", namespace="/logs")
    # def send_log(lines: list[str]):
    #     # print("user connected")
    #     # logs = ["some line 1", "some line 2"]
    #     # socketio.emit("new_log", {"logs": logs}, namespace="/logs")
    #     # socketio.call("new_log", data={"logs": logs}, namespace="/logs")
