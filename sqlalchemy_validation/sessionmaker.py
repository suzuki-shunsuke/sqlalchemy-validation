import sqlalchemy as sa

from .error import *
from .validate_table import TableValidator


class sessionmaker(sa.orm.sessionmaker):
    def __init__(self, bind=None, class_=sa.orm.session.Session,
                 autoflush=True, autocommit=False, expire_on_commit=True,
                 info=None, tables={}, **kw):
        super(sessionmaker, self).__init__(
            bind, class_, autoflush, autocommit,
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
                except ValidationError as e:
                    new_errors.append(e)
            # Before Update
            dirty_errors = []
            for model in session.dirty:
                table = model.__table__
                try:
                    validators[table.name].validate_update(session, model)
                except ValidationError as e:
                    dirty_errors.append(e)
            # Before Delete
            deleted_errors = []
            # for model in session.deleted:
            #     table = model.__table__
            #     try:
            #         validators[table.name].validate_delete(session, model)
            #     except ValidationError as e:
            #         deleted_errors.append(e)
            if new_errors or dirty_errors or deleted_errors:
                raise BeforeCommitError(new=new_errors, dirty=dirty_errors,
                                        deleted=deleted_errors)
            # Before Update
            # dirty
            # Primary Key Constraint
            # Unique Key Constraint
            # ForeignKey Constraint

            # Before Delete
            # deleted
            # ForeignKey Constraint
