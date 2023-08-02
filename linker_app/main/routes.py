import flask
from flask import render_template, request, flash

from linker_app import socketio, log_buffer, counter  # noqa F401
from linker_app.main import bp
from linker_app.main.forms import UrlForm
from linker_app.main.service.routes_handlers import link_handler
from linker_app.main.exceptions import UrlValidationError, SaveToDatabaseError

app = flask.current_app


@bp.route("/")
@bp.route("/index")
def index():  # put application's code here
    app.logger.warning("User visit index page")
    # return render_template(os.path.join(BASE_PATH, 'templates', 'index.html'))
    return render_template("index.html")


@bp.route("/links", methods=["GET", "POST"])
def links():
    template_name = 'links.html'

    app.logger.info("User visit links page")
    url_form = UrlForm()
    context = {
        "links": {},
    }
    if request.method == "POST":
        app.logger.info("Post method call")
        # if message from url form
        if url_form.validate_on_submit():
            # validate link and send it to db
            try:
                link_handler(url_form.link.data)
            except (UrlValidationError, SaveToDatabaseError) as e:
                # flush message to client about error
                flash(e.args[0])
                return render_template(template_name, url_form=url_form, context=context), 400

            flash("Link saved successfully")
            url_form = UrlForm()
            return render_template(template_name, url_form=url_form, context=context), 201
        else:
            flash("Value is not a url.")
            return render_template(template_name, url_form=url_form, context=context), 400

    return render_template(template_name, url_form=url_form, context=context)


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
    # TODO: add logger here
    app.logger.error(e)
