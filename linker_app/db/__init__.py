from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from linker_app import app
from linker_app.db.schema import metadata
from linker_app.db.engine import create_db_engine


# def init_engine():
#     engine = create_db_engine()
#     with Session(engine) as session:
#         # try:
#         result = session.execute(text("SELECT 1"))
#         print(result)
#         print("connection work correctly")
#         # except SQLAlchemyError:
#         #     print('Cant,t connect to SQLAlchemy')
