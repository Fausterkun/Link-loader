import flask
from flask import render_template, request, flash

from linker_app import socketio, log_buffer, counter  # noqa F401
from linker_app.main import bp
from linker_app.main.forms import UrlForm
from linker_app.main.service.routes_handlers import link_handler

app = flask.current_app


@bp.route("/")
@bp.route("/index")
def index():  # put application's code here
    app.logger.warning("User visit index page")
    # return render_template(os.path.join(BASE_PATH, 'templates', 'index.html'))
    return render_template("index.html")


@bp.route("/links", methods=["GET", "POST"])
def links():
    app.logger.info("User visit links page")
    url_form = UrlForm()
    # file_form =
    context = {
        "links": {},
    }
    if request.method == "POST":
        app.logger.info("Post method call")
        # if message from url form
        if url_form.validate_on_submit():
            # validate link and send it to db
            status, errors = link_handler(url_form.link.data)
            if not status:
                # TODO: add flush notification about error here
                return render_template("links.html", url_form=url_form, errors=errors, context=context)
            flash("Link saved successfully")
            app.logger.info('Links saved successfully')
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
