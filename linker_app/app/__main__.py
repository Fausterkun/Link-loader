import argparse

from configargparse import ArgumentParser

from linker_app.app import bp, socketio, app, log_buffer
from linker_app.app.settings import configure_app, init_socketio
from linker_app.utils.argparse import positive_int

ENV_VAR_PREFIX = "LINKER_APP"

parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    allow_abbrev=False,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

group = parser.add_argument_group("App options")
group.add_argument(
    "--config-file", default="config.yaml", help="Url for .yaml config file"
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
    "--message-queue", default="redis://", help="Url for message queue volume"
)
group.add_argument(
    "--channel", default="linker_socketio", help="Channel name for message queue"
)

def main():
    args = parser.parse_args()

    if args.message_queue.startswith("redis"):
        # Patch eventlet for use with redis as mq
        import eventlet

        eventlet.monkey_patch()

    configure_app(app, conf_file=args.config_file)

    init_socketio(
        socketio,
        app,
        message_queue=args.message_queue,
        port=args.port,
        channel=args.channel,
    )
    app.register_blueprint(bp)

    app.logger.info(f"App {app.name} started.")
    socketio.run(app, host=args.host, port=args.port)
    app.logger.info("App closed.")


if __name__ == "__main__":
    main()
