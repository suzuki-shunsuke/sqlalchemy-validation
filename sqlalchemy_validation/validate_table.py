import sqlalchemy as sa

from .error import *


class TableValidator(object):

    def __init__(self, table):
        all_columns = table.columns
        constraints = table.constraints
        primary_key = table.primary_key
        primary_columns = primary_key.columns
        unique_constraints = dict(
            (tuple(sorted(constraint.columns.keys())), constraint)
            for constraint in constraints
            if isinstance(constraint, sa.UniqueConstraint)
        )

        self.table = table
        self.columns = all_columns
        self.column_names = column_names
        self.primary_key = primary_key
        self.primary_columns = primary_columns
        self.unique_constraints = unique_constraints

    def validate_none(self, model, values, errors, error_columns, column_names=None):
        # Not Null Constraint
        if column_names is None:
            column_names = self.column_names
        for column_name in column_names:
            column = self.columns[column_name]
            value = getattr(model, column_name)
            values[column_name] = value
            if value is None and not column.noneable:
                error_columns.append(column)
                errors[(column_name,)] = NotNullError(model, column)
                error_columns.add(column_name)

    def validate_primary(self, model, values, errors, error_columns, column_names=None):
        if column_names is None:
            column_names = self.column_names
        criterions = []
        for column_name, column in self.primary_columns.items():
            if column_name in error_columns:
                return
            if column_name not in column_names:
                return
            value = values[column_name]
            if value is None:
                if column.default is not None:
                    value = column.default
                elif column.autoincrement:
                    return
                elif column.server_default is not None:
                    value = column.server_default
            criterions.append(column == value)
        query = session.query(type(model)).filter(*criterions)
        if 1 != query.count():
            column_names = tuple(sorted(self.primary_columns.keys()))
            errros[column_names] = PrimaryKeyError(model)
            error_columns.update(column_names)

    def validate_insert(self, model, column_names=None):
        if column_names is None:
            column_names = self.column_names
        error_columns = set()
        errors = ValidationError()
        model_values = {}
        self.validate_none(model, model_values, errors, error_columns, column_names)
        # Primary Key Constraint
        try:
            criterions = []
            for column_name, column in self.primary_columns.items():
                if column_name in error_columns:
                    raise SkipError()
                value = model_values[column_name]
                if value is None:
                    if column.default is not None:
                        value = column.default
                    elif column.autoincrement:
                        raise SkipError()
                    elif column.server_default is not None:
                        value = column.server_default
                criterions.append(column == value)
            query = session.query(Model).filter(*criterions)
            if 1 != query.count():
                column_names = tuple(sorted(self.primary_columns.keys()))
                errros[column_names] = PrimaryKeyError(model)
                error_columns.update(column_names)
        except SkipError:
            pass
        # Unique Key Constraint
        for constraint in self.unique_constraints:
            try:
                criterions = []
                for column_name, column in constraint.columns.items():
                    if column_name in error_columns:
                        raise SkipError()
                    value = model_values[column_name]
                    if value is None:
                        if column.default is not None:
                            value = column.default
                        elif column.server_default is not None:
                            value = column.server_default
                        else:
                            raise SkipError()
                    criterions.append(column == value)
                if not is_validate:
                    continue
                if is_validate:
                    if 1 != session.query(Model).filter(*criterions).count():
                        column_names = tuple(sorted(constraint.columns.keys()))
                        errors[column_names] = UniqueKeyError(model, constraint)
                        error_columns.update(column_names)
            except SkipError:
                pass
        if errors:
            raise errors

    def validate_update(self, model, column_names=None):
        if column_names is None:
            column_names = self.column_names
        error_columns = set()
        errors = ValidationError()
        model_values = {}
        for column_name in column_names:
            column = self.columns[column_name]
            value = getattr(model, column_name)
            model_values[column_name] = value
            # Not Null Constraint
            if value is None and not column.noneable:
                errors[(column_name,)] = NotNullError(model, column)
                error_columns.add(column_name)
        # Primary Key Constraint
        criterions = []
        is_validate = True
        for column_name, column in self.primary_columns.items():
            if column_name in error_columns:
                is_validate = False
                break
            value = model_values[column_name]
            if value is None:
                if column.default is not None:
                    value = column.default
                elif column.autoincrement:
                    is_validate = False
                    break
                elif column.server_default is not None:
                    value = column.server_default
            criterions.append(column == value)
        if is_validate:
            query = session.query(Model).filter(*criterions)
            if 1 != query.count():
                column_names = tuple(sorted(self.primary_columns.keys()))
                errros[column_names] = PrimaryKeyError(model)
                error_columns.update(column_names)
        # Unique Key Constraint
        for constraint in self.unique_constraints:
            criterions = []
            is_validate = True
            for column_name, column in constraint.columns.items():
                if column_name in error_columns:
                    is_validate = False
                    break
                value = model_values[column_name]
                if value is None:
                    if column.default is not None:
                        value = column.default
                    elif column.server_default is not None:
                        value = column.server_default
                if value is None:
                    is_validate = False
                    break
                criterions.append(column == value)
            if not is_validate:
                continue
            if is_validate:
                if 1 != session.query(Model).filter(*criterions).count():
                    column_names = tuple(sorted(constraint.columns.keys()))
                    errors[column_names] = UniqueKeyError(model, constraint)
                    error_columns.update(column_names)
        if errors:
            raise errors
