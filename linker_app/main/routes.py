from flask import render_template, request, current_app
from flask_wtf.csrf import CSRFError

from linker_app import socketio, log_buffer  # noqa F401
from linker_app.main import bp
from linker_app.main.forms import UrlForm, FileForm
from linker_app.database.query import get_links
from linker_app.service.handlers import link_form_handler, file_form_handler
from linker_app.utils.config import FILE_MAX_SIZE

app = current_app


@bp.route("/")
@bp.route("/index")
def index():  # put application's code here
    app.logger.warning("User visit index page")
    return render_template("index.html")


@bp.route("/links", methods=["GET", "POST"])
def links():
    template_name = "links.html"
    status_code = 200
    app.logger.info("User visit links page")
    url_form = UrlForm()
    file_form = FileForm(max_file_size=FILE_MAX_SIZE)
    if url_form.is_submitted() and 'submit_link' in request.form:
        app.logger.info("Post method call")
        url_form, url_form_success = link_form_handler(url_form)
        status_code: int = 201 if url_form_success else 400

    if file_form.is_submitted() and 'submit_file' in request.form:
        file_form, form_success = file_form_handler(file_form)
        status_code: int = 201 if form_success else 400

    # get paginated links
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    links = get_links(page=page, per_page=per_page)
    return render_template(template_name, url_form=url_form, file_form=file_form, links=links), status_code


@bp.route("/logs", methods=["GET"])
def logs():
    app.logger.info("User visit logs page")
    return render_template("logs.html")


@bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


# ------------- Websocket dynamic log notifications ------------------


@socketio.on("connect", namespace="/logs")
def connect():
    last_logs = log_buffer.get_last()
    socketio.emit(
        event="init_logs",
        to=getattr(request, "sid", None),
        data={"logs": last_logs},
        namespace="/logs",
    )


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def socketio_error_handler(e):
    # TODO: add logger here
    app.logger.error(e)
