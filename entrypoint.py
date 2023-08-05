import os

print("Flask debug: ", os.environ.get("FLASK_DEBUG"))
if not os.environ.get("FLASK_DEBUG"):
    # patch eventlet for correct work of socketio and redis
    print("Patched eventlet")
    import eventlet

    eventlet.monkey_patch()

from linker_app import create_app  # noqa E402

if __name__ == "__main__":
    app = create_app()

    port = app.config["PORT"]
    host = app.config["HOST"]

    app.extensions["socketio"].run(app, port=port, host=host)
