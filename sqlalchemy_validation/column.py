"""

"""

import sqlalchemy


class Column(sqlalchemy.Column):
    """
    """
    def __init__(self, *args, **kwargs):
        """This constructor receive additional keyword arguments
        to define additional validations.

        *args
          These arguments is passed to the sqlalchemy.Column contructor.

        **kwargs
          size: Define the size validation.
            tuple (min, max)
          length: Define the length validation.
            tuple (min, max)
            This param only works on string columns.
          reqexp: Define the RegExp validation.
            re.RegexObject
          format: Define the format validation.
            ENUM("email")
        """
        self.size = kwargs.pop("size", None)
        self.regexp = kwargs.pop("regexp", None)
        self.length = kwargs.pop("length", None)
        self.format = kwargs.pop("format", None)
        if "autoincrement" not in kwargs:
            kwargs["autoincrement"] = False
        super(Column, self).__init__(*args, **kwargs)
        self.noneable = (self.nullable or self.server_default is not None or
                         self.default is not None or self.autoincrement)

        type_length = getattr(self.type, "length", None)
        if type_length:
            if self.length is None:
                self.length = (None, type_length)
            elif self.length[1] is None:
                self.length = (self.length[0], type_length)
