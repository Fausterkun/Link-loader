from sqlalchemy import create_engine
from linker_app.app import app


def create_db_engine():
    print('create db engine')
    db = create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'],
        pool_size=app.config['SQLALCHEMY_POOL_SIZE'],
        max_overflow=app.config['SQLALCHEMY_MAX_OVERFLOW'],
        pool_timeout=app.config['SQLALCHEMY_TIMEOUT'],
        echo=True,
        echo_pool=True
    )
    return db

# engine = create_db_engine(app)

# def teardown_db(errors):
#     print('errors: ', errors)
#     print('teardown_db called')
#     db = g.pop('db', None)
#     if db is not None:
#         print('db is closed')
#         db.dispose()
