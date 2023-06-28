# from flask import render_template, request, g, redirect, url_for
from main import app


@app.route("/")
@app.route("/index")
def hello_world():  # put application's code here
    app.logger.warning("Visit index ")
    return str(app.config.items())


@app.route("/links", methods=["GET", "POST"])
def links():
    app.logger.debug("Visit links")
    return "ok"


@app.route("/logs", methods=["GET"])
def logs():
    app.logger.info("Visit logs")
    return "ok"
