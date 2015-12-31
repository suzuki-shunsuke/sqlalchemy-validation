import sys
import os

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "validate_enum"
    id = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    c1 = sav.Column(sa.Enum("foo", "bar"))


def test_func1():
    assert sav.validate(User, "c1", "foo") == "foo"


def test_func2():
    with pytest.raises(sav.EnumError):
        sav.validate(User, "c1", "1")


def test_func3():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "c1", 1)
