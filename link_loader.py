from linker_app import app, socketio

if __name__ == "__main__":
    app.logger.info(f"App {app.name} started.")
    socketio.run(app, host='0.0.0.0')  # allow_unsafe_werkzeug=True)
    app.logger.info("app closed")
