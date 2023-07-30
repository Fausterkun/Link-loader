from flask import Blueprint

bp = Blueprint("main", __name__)

from linker_app.main import routes
