import sqlalchemy as sa

from .error import *


class sessionmaker(sa.orm.sessionmaker):
    def __init__(self, bind=None, class_=sa.orm.session.Session,
                 autoflush=True, autocommit=False, expire_on_commit=True,
                 info=None, tables={}, **kw):
        super(sessionmaker, self).__init__(
            self, bind, class_, autoflush, autocommit,
            expire_on_commit, info, **kw
        )

        validators = {}
        for table_name, table in tables.items():
            validators[table_name] = TableValidator(table)

        @sa.event.listens_for(self, "before_commit")
        def before_commit(session):
            # Before Insert
            new_errors = []
            for model in session.new:
                table = model.__table__
                try:
                    validators[table.name].validate_insert(session, model)
                except BaseValidator as e:
                    new_errors.append(e)
            # Before Update
            dirty_errors = []
            for model in session.dirty:
                table = model.__table__
                try:
                    validators[table.name].validate_update(session, model)
                except BaseValidator as e:
                    dirty_errors.append(e)
            # Before Delete
            deleted_errors = []
            for model in session.deleted:
                table = model.__table__
                try:
                    validators[table.name].validate_delete(session, model)
                except BaseValidator as e:
                    deleted_errors.append(e)
            if new_errors or dirty_errors deleted_errors:
                raise BeforeCommitError(new=new_errors, dirty=dirty_errors,
                                        deleted=deleted_errors)

                columns = table.columns
                constraints = table.constraints
                primary_key = table.primary_key
                Model = type(model)
                values = {}
                for column_name, column in columns.items():
                    value = getattr(model, column_name)
                    values[column_name] = value
                    # Not Null Constraint
                    if value is None and not column.noneable:
                        raise NotNullError(model, column)
                # Primary Key Constraint
                criterions = []
                is_validate = True
                for column_name, column in primary_key.columns.items():
                    value = values[column_name]
                    if value is None:
                        if column.autoincrement:
                            is_validate = False
                            break
                        if column.default is not None:
                            value = column.default
                        elif column.server_default is not None:
                            value = column.server_default
                    criterions.append(column == value)
                if is_validate:
                    query = session.query(Model).filter(*criterions)
                    if 1 != query.count():
                        raise PrimaryKeyError(model)
                # Unique Key Constraint
                for constraint in constraints:
                    if not isinstance(constraint, sa.UniqueConstraint):
                        continue
                    criterions = []
                    is_validate = True
                    for column_name, column in constraint.columns.items():
                        value = values[column_name]
                        if value is None:
                            if column.default is not None:
                                value = column.default
                            elif column.server_default is not None:
                                value = column.server_default
                        if value is None:
                            is_validate = False
                            continue
                        criterions.append(column == value)
                    if not is_validate:
                        continue
                if is_validate:
                    if 0 != session.query(Model).filter(*criterions).count():
                        raise UniqueKeyError(model, columns, values)

            # Before Update
            # dirty
            # Primary Key Constraint
            # Unique Key Constraint
            # ForeignKey Constraint

            # Before Delete
            # deleted
            # ForeignKey Constraint
