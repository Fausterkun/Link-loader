import os

if not os.environ.get("FLASK_DEBUG"):
    # patch eventlet for correct work of socketio and redis
    import eventlet

    eventlet.monkey_patch()

from linker_app import create_app

if __name__ == "__main__":
    app = create_app()

    port = app.config["PORT"]
    host = app.config["HOST"]

    app.extensions["socketio"].run(
        app, port=port, host=host
    )  # , cors_allowed_origins=cors_allowed_origins)
    # socketio.run(app, port=8000, host='0.0.0.0', cors_allowed_origins="*")
