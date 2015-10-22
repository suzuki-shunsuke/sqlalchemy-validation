import os
import sys

import pytest

print(os.getcwd())
print(__file__)

sys.path.append(
    os.path.join(os.path.dirname(__file__), '../sqlalchemy_validation')
)
print(sys.path)

from sqlalchemy_validation import Model
from error import *

sys.path.pop()


class User(Model):
    __tablename__ = 'user'
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
    __tablename__ = 'user2'
    id = Column(mysql.INTEGER)
    name = Column(mysql.VARCHAR(20))
    pk = PrimaryKeyConstraint(id, name)
    unique1 = Column(mysql.INTEGER, unique=True)
    unique2 = Column(mysql.INTEGER)
    unique3 = Column(mysql.INTEGER)
    uniques = UniqueConstraint(unique2, unique3)


class TestUser(object):

    def test_type_error(self):
        with pytest.raises(InvalidTypeError):
            user = User(name=1)
