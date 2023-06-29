from main import app, socketio

# noinspection PyUnresolvedReferences
# from main import routes

if __name__ == "__main__":
    app.logger.info(f"App {app.name} started.")
    socketio.run(app, allow_unsafe_werkzeug=True)
    app.logger.info("app closed")
