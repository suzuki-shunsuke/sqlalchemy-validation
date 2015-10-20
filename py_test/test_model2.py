from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint, \
    CheckConstraint
from sqlalchemy import ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    @validates('password')
    def validate_password(self, colmn_name, value):
        return value


def validate_length(target, value, oldvalue, initiator):
    if len(value) < 3:
        raise ValueError('Too short')


def validate_type(model, column_name, value):
    print(target)
    Model = target.class_
    column_name = target.key
    table = Model.__table__
    columns = table.columns
    column = columns[column_name]
    if isinstance(value, column.python_type):
        raise TypeError()


@event.listens_for(User, 'mapper_configured')
def receive_mapper_configured(mapper, class_):
    table = class_.__table__
    columns = table.columns



    for column_name in columns.keys():
        event.listen(getattr(class_, column_name), "set", validate_length)
        event.listen(getattr(class_, column_name), "set", validate_type)
