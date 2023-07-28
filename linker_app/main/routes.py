import json

import flask
from flask import render_template, request, jsonify

from linker_app import socketio, log_buffer, counter  # noqa F401
from linker_app.main import bp


# from linker_app.app.service.routes_handlers import handle_link

app = flask.current_app

@bp.route("/")
@bp.route("/index")
def index():  # put application's code here
    app.logger.warning("User visit index page")
    # return render_template(os.path.join(BASE_PATH, 'templates', 'index.html'))
    return render_template("index.html")


# @bp.route("/links", methods=["GET", "POST"])
# def links():
#     """ Route for links:
#     Get:
#         - Get all links
#     Post: - used form-identifier for indicate which from used
#         If str received:
#             - parse it, add to db(if no errors) and return parse result/errors
#
#         If file received:
#             # TODO : continue
#             -
#     """
#     if request.method == 'POST':
#         data_type = request.form['form-identifier']
#         if data_type == 'link':
#             resp = handle_link(request.form['link-inpt'])
#             print('handle post to link', resp)
#             return jsonify(resp)
#         # elif data_type == 'file':
#         #     print('file handlde')
#         #     print('handle post to file')
#         #     return json.dumps({'file': 'works'})
#         else:
#             return json.dumps({"logs": 'none'})
#
#     app.logger.info("User visit links page")
#     # get all links
#     context = {"links": {}}
#     return render_template("links.html", context=context)
#
#

# @bp.route("/links", methods=["GET", "POST"])
# def links():
#     app.logger.info("User visit links page")
#     return "<h1>hi max</h1>"


@bp.route("/logs", methods=["GET"])
def logs():
    global counter
    app.logger.info(str(counter))
    counter += 1
    return render_template("logs.html")


# ------------- Websocket dynamic log notifications ------------------


@socketio.on("connect", namespace="/logs")
def connect():
    app.logger.info("Websocket connection to /logs page")
    # collect all previous logs
    # logs = app.log_buffer.get_all()
    logs = log_buffer.get_all()
    socketio.emit(
        event="init_logs",
        to=getattr(request, "sid", None),
        data={"logs": logs},
        namespace="/logs",
    )
