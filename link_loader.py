from main import app

# noinspection PyUnresolvedReferences
from main import routes

if __name__ == "__main__":
    app.logger.info(f"App {app.name} started.")
    app.run()
    app.logger.info("app closed")
