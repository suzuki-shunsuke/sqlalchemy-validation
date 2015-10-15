"""

"""


class BaseValidationError(Exception):
    pass


class ValidationError(BaseValidationError):
    """
    """
    def __init__(self, errors):
        """
        """
        self.errors = errors
        super(ValidationError, self).__init__()

    def __str__(self):
        return ("The following validation errors have occured.\n\n"
                "\n\n".join(str(error) for error in self.errors))


class ConstraintError(BaseValidationError):
    """
    """
    def __init__(self, model, items):
        """
        """
        self.model = model
        self.values = items


class PrimaryKeyError(ConstraintError):
    """Primary Key Constraint.
    """

    def __str__(self):
        return ("PrimaryKeyError!\n"
                "Table: {}\n"
                "column: value\n"
                "{}").format(
            type(self.model).__name__,
            "\n".join("{}: {}".format(column_name, value)
                      for column_name, value in self.items.items())
        )


class UniqueKeyError(ConstraintError):
    """Unique Key Constraint.
    """
    def __str__(self):
        return ("UniqueKeyError!\n"
                "Table: {}\n"
                "column: value\n"
                "{}").format(
            type(self.model).__name__,
            "\n".join("{}: {}".format(column_name, value)
                      for column_name, value in self.items.items())
        )


class ValidatesError(BaseValidationError):
    """
    """
    def __init__(self, model, column, value):
        """
        """
        self.model = model
        self.column = column
        self.value = value


class EnumError(ValidatesError):
    """Enum Constraint.
    """
    def __str__(self):
        return ("EnumError!\nTable.column: {}.{}\n"
                "Enum: {}\nvalue: {}").format(
            type(self.model).__name__, self.column.name,
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
            type(self.model).__name__, self.column.name,
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
            type(self.model).__name__, self.column.name,
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
            type(self.model).__name__, self.column.name,
            self.column.size, self.value
        )


class OverMinError(ValidatesError):
    """Size Constraint.
    """
    def __str__(self):
        return ("OverMinError!\n"
                "Table.column: {}.{}\n"
                "size limitation: {}\n"
                "value: {}").format(
            type(self.model).__name__, self.column.name,
            self.column.size, self.value
        )


class NotNullError(ValidatesError):
    """Not Null Constraint.
    """
    def __str__(self):
        return ("NotNullError!\n""{}.{} can't be None.").format(
            type(self.model).__name__, self.column.name
        )


class InvalidTypeError(ValidatesError):
    """Type Constraint.
    """
    def __str__(self):
        return ("TypeError! {}.{} must be {} object, "
                "but {} is {} object.").format(
            type(self.model).__name__, self.column.name,
            self.column.type.python_type, self.value, type(self.value)
        )
        return ("InvalidTypeError!\n"
                "Table.column: {}.{}\n"
                "expected type: {}\n"
                "value(type): {}({})").format(
            type(self.model).__name__, self.column.name,
            self.column.type.python_type, self.value, type(self.value)
        )


class EmailError(ValidatesError):
    """Email Format Constraint.
    """
    def __str__(self):
        return ("EmailError! {}.{} must be an email address, "
                "but {} isn't.").format(
            type(self.model).__name__, self.column.name, self.value
        )
        return ("EmailError!\n"
                "Table.column: {}.{}\n"
                "value: {}").format(
            type(self.model).__name__, self.column.name,
            self.value
        )


class RegExpError(ValidatesError):
    """RegExp Constraint.
    """
    def __str__(self):
        return ("RegExpError!\n"
                "Table.column: {}.{}\n"
                "RegExp: {}\n"
                "value: {}").format(
            type(self.model).__name__, self.column.name,
            self.column.regexp, self.value
        )
