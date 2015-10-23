import sqlalchemy

from .error import *


class ColumnValidator(object):

    def __init__(self, column):
        self.column = column
        self.type = column.type
        self.python_type = column.type.python_type
        validates = []
        validates.append(self.validate_type)
        if isinstance(column.type, sqlalchemy.types.Enum):
            self.enums = column.type.enums
            validates.append(self.validate_enum)
        if self.python_type is str:
            length = getattr(column, "length", False)
            if length:
                self.length = length
            else:
                self.length = (None, self.type.length)
            validates.append(self.validate_length)
            regexp = getattr(column, "regexp", False)
            if regexp:
                self.regexp = regexp
                validates.append(self.validate_regexp)
            format = getattr(column, "format", False)
            if format == "email":
                validates.append(self.validate_email)
        size = getattr(column, "size", False)
        if size:
            self.size = size
            validates.append(self.validate_size)
        self.validates = validates

    def validate(self, model, value):
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
          value: The validated value.

        Return:
          None

        Raises:
          sqlalchemy_validation.NotNullError: Not Null Constraint
          sqlalchemy_validation.InvalidTypeError: Type Constraint
          sqlalchemy_validation.TooLongError, TooShortError: Length Consraint
          sqlalchemy_validation.RegExpError: RegExp Consraint
          sqlalchemy_validation.EmailError: Email Constraint
          sqlalchemy_validation.OverMinError, OverMaxError: Size Constraint
        """
        if value is None:
            if self.column.noneable:
                return
            raise NotNullError(model, self.column)
        for validate in self.validates:
            validate(model, value)

    def validate_enum(self, model, value):
        '''Enum Constraint
        '''
        if value not in self.enums:
            raise EnumError(model, self.column, value)

    def validate_type(self, model, value):
        '''Type Constraint
        '''
        if not isinstance(value, self.python_type):
            raise InvalidTypeError(model, self.column, value)

    def validate_length(self, model, value):
        '''Length Constraint
        '''
        length = len(value)
        m, M = self.length
        if m and length < m:
            raise TooShortError(model, self.column, value)
        if M and length > M:
            raise TooLongError(model, self.column, value)

    def validate_regexp(self, model, value):
        '''RegExp Constraint
        '''
        if self.regexp.match(value) is None:
            raise RegExpError(model, self.column, value)

    def validate_email(self, model, value):
        '''Format Constraint
        '''
        import validate_email
        if validate_email.validate_email(value):
            raise EmailError(model, self.column, value)

    def validate_size(self, model, value):
        '''Size Constraint
        '''
        m, M = self.size
        if m and value < m:
            raise OverMinError(model, self.column, value)
        if M and value > M:
            raise OverMaxError(model, self.column, value)
