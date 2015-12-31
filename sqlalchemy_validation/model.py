from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta

from .error import BaseValidationError, ValidationError
from .attribute import validate_attribute


class MetaClass(DeclarativeMeta):
    """
    """

    def __init__(cls, classname, bases, dict_):
        """
        """
        super(MetaClass, cls).__init__(classname, bases, dict_)
        if hasattr(cls, "__table__"):
            validate_attribute(cls)


def _table_columns(constraint, table):
    return "{}__{}".format(
        table.name, "__".join(sorted(constraint.columns.keys()))
    )


metadata = MetaData(naming_convention={
    "table_columns": _table_columns,
    "ix": "ix_%(table_columns)s",
    "uq": "uq_%(table_columns)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})


class BaseModel(object):
    """
    """

    def __init__(self, **kwargs):
        """
        Args:
          kwargs:

        Raises:
          TypeError:
          sqlalchemy_validation.ValidationError
        """
        cls_ = type(self)
        errors = ValidationError()
        for column_name, value in kwargs.items():
            if not hasattr(cls_, column_name):
                raise TypeError(
                    "{!r} is an invalid keyword argument for {!s}".format
                    (column_name, cls_.__name__))
            try:
                setattr(self, column_name, value)
            except BaseValidationError as e:
                errors[(column_name,)] = e
        if errors:
            raise errors

    def __call__(self, **kwargs):
        """Sets kwargs to model's columns and returns self.

        Args:

        Returns:
          self

        Raises:
          TypeError:
          sqlalchemy_validation.ValidationError
        """
        self.__init__(**kwargs)
        return self


Model = declarative_base(cls=BaseModel, constructor=None, metaclass=MetaClass, metadata=metadata)
