import sqlalchemy
from sqlalchemy.schema import UniqueConstraint, PrimaryKeyConstraint, MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative.api import DeclarativeMeta

from .validate_column import create_validate_column
from .error import *


def _union_validates(validate1, validate2):
    """
    """

    def wrap(model, column_name, value):
        val = validate1(model, column_name, value)
        return validate2(model, column_name, val)

    return wrap


class Meta(DeclarativeMeta):
    """
    """

    def __init__(cls, classname, bases, dict_):
        """
        """
        super(Meta, cls).__init__(classname, bases, dict_)
        if hasattr(cls, "__table__"):
            for column in cls.__table__.columns:
                column.noneable = (
                    column.nullable or
                    column.server_default is not None or
                    column.default is not None or
                    column.autoincrement)

    def __new__(cls, name, bases, namespace, **kwargs):
        """
        """
        if "__tablename__" not in namespace:
            return DeclarativeMeta.__new__(
                cls, name, bases, namespace, **kwargs
            )
        validates = {}
        for column_name, column in namespace.items():
            if not isinstance(column, sqlalchemy.Column):
                continue
            validate_name = "_validate_{}".format(column_name)
            _validate = create_validate_column(column)
            if validate_name in namespace:
                _validate = _union_validates(
                    _validate, namespace[validate_name]
                )
            validates[validate_name] = sqlalchemy.orm.validates(column_name)(
                _validate
            )
        namespace.update(validates)
        return DeclarativeMeta.__new__(cls, name, bases, namespace, **kwargs)


def _validate_unique(model, session, columns, values):
    criterions = []
    for name, column in columns.items():
        value = values[name]
        if value is None:
            if column.autoincrement:
                return model
            if column.default is not None:
                value = column.default
            elif column.server_default is not None:
                value = column.server_default
            if value is None:
                return model
        criterions.append(column == value)
    if 0 != session.query(type(model)).filter(*criterions).count():
        raise UniqueKeyError(model, columns, values)
    return model


def _validate_primary(model, session, columns, values):
    criterions = []
    for name, column in columns.items():
        value = values[name]
        if value is None:
            if column.autoincrement:
                return model
            if column.default is not None:
                value = column.default
            elif column.server_default is not None:
                value = column.server_default
        criterions.append(column == value)
    if 0 != session.query(type(model)).filter(*criterions).count():
        raise PrimaryKeyError(model, columns, values)
    return model


def _table_columns(constraint, table):
    return "{}__{}".format(
        table.name, "__".join(sorted(constraint.columns.keys()))
    )


@as_declarative(
    metaclass=Meta, constructor=None,
    metadata=MetaData(naming_convention={
        "table_columns": _table_columns,
        "ix": "ix_%(table_columns)s",
        "uq": "uq_%(table_columns)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })
)
class Model(object):
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
        errors = []
        for column_name, value in kwargs.items():
            if not hasattr(cls_, column_name):
                raise TypeError(
                    "{!r} is an invalid keyword argument for {!s}".format
                    (column_name, cls_.__name__))
            try:
                setattr(self, column_name, value)
            except BaseValidationError as e:
                errors.append(e)
        if errors:
            raise ValidationError(errors)

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

    def validate_insert(self, session, column_names=None):
        """Validate whether this model can be inserted or not.

        Args:
          session: Session object.

        Returns:
          self

        Raises:
          sqlalchemy_validation.ValidationError
        """
        table = self.__table__
        constraints = table.constraints
        if column_names is None:
            column_names = table.columns.keys()
        errors = []
        nulls = []
        values = dict((column_name, getattr(self, column_name))
                      for column_name in column_names)
        for column_name, value in values.items():
            column = table.columns[column_name]
            if not column.noneable and value is None:
                errors.append(NotNullError(self, column))
                nulls.append(column_name)
        for constraint in constraints:
            columns = constraint.columns
            names = columns.keys()
            extracted_values = dict((name, values[name]) for name in names)
            if any(name in nulls for name in names):
                continue
            try:
                if isinstance(constraint, PrimaryKeyConstraint):
                    _validate_primary(self, session, columns, extracted_values)
                elif isinstance(constraint, UniqueConstraint):
                    _validate_unique(self, session, columns, extracted_values)
            except BaseValidationError as e:
                errors.append(e)
        if errors:
            raise ValidationError(errors)

        return self
