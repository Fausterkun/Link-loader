from main import app

# noinspection PyUnresolvedReferences
from main import routes

if __name__ == "__main__":
    app.run()
    app.logger.info(f"App {app.name} started.")
