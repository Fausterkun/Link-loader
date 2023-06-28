from main.app import create_app, configure_logging

app = create_app()
configure_logging(app)
