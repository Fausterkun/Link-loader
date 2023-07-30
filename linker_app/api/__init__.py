from flask import Blueprint

bp = Blueprint("api", __name__)

from linker_app.api import routes
