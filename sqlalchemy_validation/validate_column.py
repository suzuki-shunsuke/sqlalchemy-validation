import sqlalchemy

from .error import *


def create_validate_column(column):
    """Returns a validation function.
    """

    def validate_column(model, column_name, value):
        """Validate the value when the model's column attribute is changed.
        This function supports the following constraints.

        * Not Null Constraint
        * Type Constraint
        * Length Constraint
        * RegExp Constraint
        * Email Constraint
        * Size Constraint

        Args:
          model: A sqlalchemy_validation.Model instance.
          column_name: A column name.
            A str object.
          value: The validated value.

        Return:
          The column's value.

        Raises:
          sqlalchemy_validation.NotNullError: Not Null Constraint
          sqlalchemy_validation.InvalidTypeError: Type Constraint
          sqlalchemy_validation.TooLongError, TooShortError: Length Consraint
          sqlalchemy_validation.RegExpError: RegExp Consraint
          sqlalchemy_validation.EmailError: Email Constraint
          sqlalchemy_validation.OverMinError, OverMaxError: Size Constraint
        """
        # Not Null Constraint
        if value is None:
            if not column.noneable:
                raise NotNullError(model, column, None)
            return value

        # Enum Constraint
        if issubclass(type(column.type), sqlalchemy.types.Enum):
            if value in column.type.enums:
                return value
            else:
                raise EnumError(model, column, value)
        else:
            # Type Constraint
            if not isinstance(value, column.type.python_type):
                raise InvalidTypeError(model, column, value)

            # String Constraint
            if column.type.python_type is str:
                # Length Constraint
                length = len(value)
                if column.length:
                    if column.length[0] and length < column.length[0]:
                        raise TooShortError(model, column, value)
                    if column.length[1] and length > column.length[1]:
                        raise TooLongError(model, column, value)

                # RegExp Constraint
                if column.regexp:
                    if column.regexp.match(value) is None:
                        raise RegExpError(model, column, value)

                # Format Constraint
                if column.format == "email":
                    import validate_email
                    if validate_email.validate_email(value):
                        raise EmailError(model, column, value)

            # Size Constraint
            if column.size:
                if column.size[0] and value < column.size[0]:
                    raise OverMinError(model, column, value)
                if column.size[1] and value > column.size[1]:
                    raise OverMaxError(model, column, value)
            return value

    return validate_column
