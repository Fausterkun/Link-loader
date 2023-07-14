from flask import render_template, request

from linker_app import app, bp, socketio, log_buffer, \
    counter  # noqa F401


@bp.route("/")
@bp.route("/index")
def index():  # put application's code here
    app.logger.warning("User visit index page")
    # return render_template(os.path.join(BASE_PATH, 'templates', 'index.html'))
    return render_template("index.html")


@bp.route("/links", methods=["GET", "POST"])
def links():
    app.logger.info("User visit links page")
    return "<h1>hi max</h1>"


@bp.route("/logs", methods=["GET"])
def logs():
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
    app.logger.info("Websocket connection to /logs page")
    # collect all previous logs
    logs = log_buffer.get_all()
    socketio.emit(
        event="init_logs",
        to=getattr(request, "sid", None),
        data={"logs": logs},
        namespace="/logs",
    )
