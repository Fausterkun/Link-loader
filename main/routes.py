from flask import render_template, request, g, redirect, url_for
from app import app


@app.route('/')
@app.route('/index')
def hello_world():  # put application's code here
    return app.config['TEST_VAR']


@app.route('/links', methods=['GET', 'POST'])
def links():
    return 'ok'


@app.route('/logs', methods=["GET"])
def logs():
    return 'ok'
