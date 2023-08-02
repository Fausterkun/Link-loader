from sqlalchemy.orm import declared_attr
from flask_sqlalchemy.model import Model
from sqlalchemy import MetaData, Integer, Column


class IdModel(Model):
    """ Base class with id initialized by default """

    @declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, "__table__", None) is not None:
                t = ForeignKey(base.id)
                break
        else:
            t = Integer

        return Column(t, primary_key=True)


# setup naming convention for equal table name due different dialects
convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
