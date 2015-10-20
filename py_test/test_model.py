import re

from sqlalchemy.dialects import mysql
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint, \
    CheckConstraint
from sqlalchemy import ForeignKey
import pytest

from .sqlalchemy_validation import Model, Column


class User(Model):
    __tablename__ = 'users'
    # primary key
    name = Column(mysql.VARCHAR(20), primary_key=True)
    # length
    name2 = Column(mysql.VARCHAR(20), length=(10, 20))
    # length
    name3 = Column(mysql.VARCHAR(20), length=(None, 20))
    # length
    name4 = Column(mysql.VARCHAR(20), length=(10, None))
    # size
    point = Column(mysql.INTEGER, size=(10, 20))
    # size
    point2 = Column(mysql.INTEGER, size=(None, 20))
    # size
    point3 = Column(mysql.INTEGER, size=(10, None))
    # regexp
    password = Column(mysql.VARCHAR(20),
                      regexp=re.compile(r'[-._0-9a-z]{4,10}'))
    # email
    email = Column(mysql.VARCHAR(50), format='email')
    # nullable
    profile = Column(mysql.VARCHAR(20), nullable=False)
    # nullable default
    profile2 = Column(mysql.VARCHAR(20), default='', nullable=False)
    # nullable server_default
    profile3 = Column(mysql.VARCHAR(20), server_default='', nullable=False)
    # nullable autoincrement
    number = Column(mysql.INTEGER, nullable=False, autoincrement=True)
    # Enum
    status = Column(mysql.ENUM('on', 'off'), nullable=False)


class User2(Model):
    __tablename__ = 'users2'
    id = Column(mysql.INTEGER)
    name = Column(mysql.VARCHAR(20))
    pk = PrimaryKeyConstraint(id, name)
    unique1 = Column(mysql.INTEGER, unique=True)
    unique2 = Column(mysql.INTEGER)
    unique3 = Column(mysql.INTEGER)
    uniques = UniqueConstraint(unique2, unique3)


class Person(Model):
    __tablename__ = 'person'
    id = Column(mysql.INTEGER, primary_key=True)
    name = Column(mysql.VARCHAR(20))
    age = Column(mysql.INTEGER)
    name2 = Column(mysql.VARCHAR(20), ForeignKey('users2.name'))
    idx = Column(mysql.INTEGER, index=True)
    check = Column(
        mysql.INTEGER, CheckConstraint(r'check < 10', name='check_max_limit')
    )

    uniques = UniqueConstraint(name, age)
    check2 = CheckConstraint(
        r'age < 10 OR idx > 20',
        name="age_max_and_idx_min"
    )


def test_model():
    user = User()
    user2 = User2()
    person = Person()
