"""
"""

from abc import ABCMeta


class BaseValidationError(Exception, metaclass=ABCMeta):
    pass


class ValidationError(dict):
    pass


BaseValidationError.register(ValidationError)


class BeforeCommitError(BaseValidationError):
    def __init__(new=None, dirty=None, deleted=None):
        self.new = new
        self.dirty = dirty
        self.deleted = deleted


class SkipError(Exception):
    pass


class PrimaryKeyError(BaseValidationError):
    """Primary Key Constraint.
    """
    def __init(self, model, values):
        self.model = model
        self.primary_key = self.model.__table__.primary_key
        self.values = values
        super(ValidationError, self).__init__()

    def __str__(self):
        return ("PrimaryKeyError!\n"
                "Table: {}\n"
                "column: value\n"
                "{}").format(
            type(self.model).__name__,
            "\n".join("{}: {}".format(column_name, value)
                      for column_name, value in values)
        )


class UniqueKeyError(BaseValidationError):
    """Unique Key Constraint.
    """
    def __init(self, model, constraint, values):
        self.model = model
        self.constraint = constraint
        self.values = values

        super(ValidationError, self).__init__()

    def __str__(self):
        return ("UniqueKeyError!\n"
                "Table: {}\n"
                "column: value\n"
                "{}").format(
            type(self.model).__name__,
            "\n".join("{}: {}".format(column_name, value)
                      for column_name, value in self.values.items())
        )


class ValidatesError(BaseValidationError):
    def __init__(self, model, column, value):
        self.model = model
        self.column = column
        self.value = value
        self.model_name = model.__class__.__name__
        super(ValidatesError, self).__init__()


class EnumError(ValidatesError):
    """Enum Constraint.
    """
    def __str__(self):
        return ("EnumError!\nTable.column: {}.{}\n"
                "Enum: {}\nvalue: {}").format(
            self.model_name, self.column.name,
            self.column.type.enums, self.value
        )


class TooShortError(ValidatesError):
    """Length Constraint.
    """
    def __str__(self):
        return ("TooShortError!\n"
                "Table.column: {}.{}\n"
                "length limitation: {}\n"
                "value(length): {}({})").format(
            self.model_name, self.column.name,
            self.column.length, self.value, len(self.value)
        )


class TooLongError(ValidatesError):
    """Length Constraint.
    """
    def __str__(self):
        return ("TooLongError!\n"
                "Table.column: {}.{}\n"
                "length limitation: {}\n"
                "value(length): {}({})").format(
            self.model_name, self.column.name,
            self.column.length, self.value, len(self.value)
        )


class OverMaxError(ValidatesError):
    """Size Constraint.
    """
    def __str__(self):
        return ("OverMaxError!\n"
                "Table.column: {}.{}\n"
                "size limitation: {}\n"
                "value: {}").format(
            self.model_name, self.column.name,
            self.column.size, self.value
        )


class OverMinError(ValidatesError):
    """Size Constraint.
    """
    def __str__(self):
        value = getattr(self.model, self.column.name)
        return ("OverMinError!\n"
                "Table.column: {}.{}\n"
                "size limitation: {}\n"
                "value: {}").format(
            self.model_name, self.column.name,
            self.column.size, self.value
        )


class NotNullError(ValidatesError):
    """Not Null Constraint.
    """
    def __str__(self):
        return ("NotNullError!\n""{}.{} can't be None.").format(
            self.model_name, self.column.name
        )


class InvalidTypeError(ValidatesError):
    """Type Constraint.
    """
    def __str__(self):
        return ("InvalidTypeError!\n"
                "Table.column: {}.{}\n"
                "expected type: {}\n"
                "value(type): {}({})").format(
            self.model_name, self.column.name,
            self.column.type.python_type, self.value, type(self.value)
        )


class EmailError(ValidatesError):
    """Email Format Constraint.
    """
    def __str__(self):
        return ("EmailError!\n"
                "Table.column: {}.{}\n"
                "value: {}").format(
            self.model_name, self.column.name, self.value
        )


class RegExpError(ValidatesError):
    """RegExp Constraint.
    """
    def __str__(self):
        return ("RegExpError!\n"
                "Table.column: {}.{}\n"
                "RegExp: {}\n"
                "value: {}").format(
            self.model_name, self.column.name, self.column.regexp, self.value
        )
