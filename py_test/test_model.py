import os
import sys
import re

import pytest
import sqlalchemy as sa

current_dir = os.path.dirname(__file__)
mysqlconfigfile = os.path.join(current_dir, 'mysql-connection.json')

sys.path.append(
    os.path.join(current_dir, '../sqlalchemy_validation')
)

from sqlalchemy_validation import Model, Column, sessionmaker
from sqlalchemy_validation.error import *

from .connection import Connection

sys.path.pop()


class User(Model):
    __tablename__ = 'user'
    # primary key
    name = Column(sa.VARCHAR(20), primary_key=True)
    # length
    name2 = Column(sa.VARCHAR(20), length=(10, 20))
    # length
    name3 = Column(sa.VARCHAR(20), length=(None, 20))
    # length
    name4 = Column(sa.VARCHAR(20), length=(10, None))
    # size
    point = Column(sa.INTEGER, size=(10, 20))
    # size
    point2 = Column(sa.INTEGER, size=(None, 20))
    # size
    point3 = Column(sa.INTEGER, size=(10, None))
    # regexp
    password = Column(sa.VARCHAR(20),
                      regexp=re.compile(r'[-._0-9a-z]{4,10}'))
    # email
    email = Column(sa.VARCHAR(50), format='email')
    # nullable
    profile = Column(sa.VARCHAR(20), nullable=False)
    # nullable default
    profile2 = Column(sa.VARCHAR(20), default='', nullable=False)
    # nullable server_default
    profile3 = Column(sa.VARCHAR(20), server_default='', nullable=False)
    # nullable autoincrement
    number = Column(sa.INTEGER, nullable=False, autoincrement=True)
    # Enum
    status = Column(sa.Enum('on', 'off'), nullable=False)


class User2(Model):
    __tablename__ = 'users2'
    id = Column(sa.INTEGER)
    name = Column(sa.VARCHAR(20))
    pk = sa.PrimaryKeyConstraint(id, name)
    unique1 = Column(sa.INTEGER, unique=True)
    unique2 = Column(sa.INTEGER)
    unique3 = Column(sa.INTEGER)
    uniques = sa.UniqueConstraint(unique2, unique3)


class TestUser(object):

    def test_type_error(self):
        with pytest.raises(ValidationError):
            user = User(name=1)
        with pytest.raises(ValidationError):
            user = User(number="foo")

    def test_length_error(self):
        with pytest.raises(ValidationError):
            user = User(name="a" * 30)

    def test_noneable(self):
        with pytest.raises(BeforeCommitError):
            user = User2()
            conn = Connection(mysqlconfigfile)
            Session = sessionmaker(conn.engine, tables=User2.metadata.tables)
            session = Session()
            session.add(user)
            session.commit()
        session.close()

    def test_primary(self):
        with pytest.raises(PrimaryKeyError):
            try:
                user = User2(id=5, name='bar')
                conn = Connection(mysqlconfigfile)
                Session = sessionmaker(conn.engine, tables=User2.metadata.tables)
                session = Session()
                session.add(user)
                session.commit()
            except BeforeCommitError as e:
                raise e.new[0]
        session.close()
