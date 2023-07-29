import os
import argparse

import sqlalchemy
from sqlalchemy import text
from configargparse import ArgumentParser

if not os.environ.get('FLASK_DEBUG'):
    # patch eventlet for correct work of socketio and redis
    import eventlet

    eventlet.monkey_patch()

from linker_app import create_app, db, ENV_VAR_PREFIX
from linker_app.utils.argparse import positive_int, clear_environ

parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    allow_abbrev=False,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

group = parser.add_argument_group("App options")
group.add_argument(
    '-c', "--config-file", default="config.yaml", help="Url for .yaml config file"
)

group = parser.add_argument_group("Server options")
group.add_argument(
    "--host", default="0.0.0.0", help="IPv4 address for server for listen"
)
group.add_argument(
    "--port", type=positive_int, default=8000, help="TCP server listening port"
)

group = parser.add_argument_group("Socketio options")
group.add_argument(
    "--message-queue", default="redis://", help="Url for message queue"
)
group.add_argument(
    "--channel", default="linker_socketio", help="Channel name at message queue"
)
group.add_argument("--cors-allowed-origins", help="Allowed cors for app to connect")
group.add_argument("--log-buffer-size", type=positive_int, help="Log buffer max size")

if __name__ == "__main__":
    args = parser.parse_args()

    if "config_file" in args:
        app = create_app(conf_file=args.config_file, args=args)
    else:
        app = create_app(args=args)

    port = app.config['PORT']
    host = app.config['HOST']
    cors_allowed_origins = app.config['CORS_ALLOWED_ORIGINS']

    app.extensions['socketio'].run(
        app,
        port=port,
        host=host,
    )
    socketio.run(app, port=8000, host='0.0.0.0')  # , cors_allowed_origins="*")
