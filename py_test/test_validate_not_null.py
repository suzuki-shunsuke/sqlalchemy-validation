import sys
import os

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "validate_not_null"
    id = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    c1 = sav.Column(sa.INTEGER, nullable=False)
    c2 = sav.Column(sa.INTEGER, nullable=False, default=5)
    c3 = sav.Column(sa.VARCHAR(5), nullable=False, server_default="foo")
    c4 = sav.Column(sa.VARCHAR(5))


class User2(sav.Model):
    __tablename__ = "validate_not_null2"
    id = sav.Column(sa.INTEGER, primary_key=True)


def test_func1():
    with pytest.raises(sav.NotNullError):
        sav.validate(User, "id", None)


def test_func2():
    with pytest.raises(sav.NotNullError):
        sav.validate(User, "c2", None)


def test_func3():
    with pytest.raises(sav.NotNullError):
        sav.validate(User, "c3", None)


def test_func4():
    assert sav.validate(User, "c4", None) is None


def test_func5():
    with pytest.raises(sav.NotNullError):
        sav.validate(User2, "id", None)
