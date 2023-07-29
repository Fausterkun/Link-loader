import json

import flask
from flask import render_template, request, jsonify

from linker_app import socketio, log_buffer, counter  # noqa F401
from linker_app.main import bp
from linker_app.main.service.routes_handlers import handle_link
from linker_app.main.forms import UrlForm

app = flask.current_app


@bp.route("/")
@bp.route("/index")
def index():  # put application's code here
    app.logger.warning("User visit index page")
    # return render_template(os.path.join(BASE_PATH, 'templates', 'index.html'))
    return render_template("index.html")


@bp.route("/links", methods=["GET", "POST"])
def links():
    """ Route for links:
    Get:
        - Get all links
    Post: - used form-identifier for indicate which from used
        If str received:
            - parse it, add to db(if no errors) and return parse result/errors

        If file received:
            # TODO : continue
            -
    """
    app.logger.info("User visit links page")
    url_form = UrlForm()
    if request.method == 'POST':
        app.logger.info('Post method call')
        if url_form.validate_on_submit():
            print(url_form.link)
    context = {"links": {}}
    return render_template("links.html", url_form=url_form, context=context)


@bp.route("/logs", methods=["GET"])
def logs():
    app.logger.info("User visit logs page")
    # app.logger.info(str(counter))
    return render_template("logs.html")


# ------------- Websocket dynamic log notifications ------------------


@socketio.on("connect", namespace="/logs")
def connect():
    last_logs = log_buffer.get_last()  # copy last logs
    socketio.emit(
        event="init_logs",
        to=getattr(request, "sid", None),
        data={"logs": last_logs[:]},
        namespace="/logs",
    )
    app.logger.info("Websocket connection to /logs page")


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    app.logger.error(e)
