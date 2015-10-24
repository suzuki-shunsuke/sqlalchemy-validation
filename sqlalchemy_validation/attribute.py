"""
"""

import sqlalchemy as sa


def set_attribute(column):
    """
    """
    def wrap(model, value, oldvalue, initiator):
        column.validator.validate(model, value)

    return wrap


def validate_attribute(Model):
    """
    """
    table = Model.__table__
    columns = table.columns
    constraints = table.constraints
    primary_key = table.primary_key
    for column_name, column in columns.items():
        attribute = getattr(Model, column_name)
        sa.event.listen(attribute, "set", set_attribute(column))
