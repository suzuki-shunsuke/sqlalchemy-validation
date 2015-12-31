import sys
import os

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "validate"
    id = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    c1 = sav.Column(sa.INTEGER, size=(None, 5))


def test_func1():
    with pytest.raises(sav.OverMaxError):
        sav.validate(User, id=3, c1=6)


def test_func2():
    assert isinstance(sav.validate(User, id=3, c1=3), User)


def test_func3():
    with pytest.raises(sav.OverMaxError):
        sav.validate(User, "c1", 6)


def test_func4():
    assert sav.validate(User, "c1", 3) == 3
