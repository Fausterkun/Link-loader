import os
import sqlalchemy
from sqlalchemy import text

if not os.environ.get('FLASK_DEBUG'):
    import eventlet

    eventlet.monkey_patch()

from linker_app import create_app
from linker_app import db

app = create_app()

if __name__ == "__main__":
    port = app.config['PORT']
    host = app.config['HOST']
    app.extensions['socketio'].run(app, port=port, host=host)
    # socketio.run(app, port=8000, host='0.0.0.0')  # , cors_allowed_origins="*")
