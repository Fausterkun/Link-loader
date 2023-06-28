from flask.config import Config


class AppConfig(Config):
    _obj = None

    # Singleton for config obj
    def __new__(cls, *args, **kwargs):
        if not cls._obj:
            cls._objs = super().__new__(*args, **kwargs)
        return cls._obj


