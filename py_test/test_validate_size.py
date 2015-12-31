import sys
import os

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "validate_size"
    id = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    c1 = sav.Column(sa.INTEGER)
    c2 = sav.Column(sa.INTEGER, size=(None, 3))
    c3 = sav.Column(sa.INTEGER, size=(1, None))
    c4 = sav.Column(sa.INTEGER, size=(1, 3))


def test_func1():
    assert sav.validate(User, "c1", 0) == 0


def test_func2():
    assert sav.validate(User, "c1", 5) == 5


def test_func4():
    assert sav.validate(User, "c2", 0) == 0


def test_func5():
    assert sav.validate(User, "c2", 3) == 3


def test_func6():
    with pytest.raises(sav.OverMaxError):
        sav.validate(User, "c2", 4)


def test_func7():
    with pytest.raises(sav.OverMinError):
        sav.validate(User, "c3", 0)


def test_func8():
    assert sav.validate(User, "c3", 1) == 1


def test_func9():
    assert sav.validate(User, "c3", 5) == 5


def test_func11():
    with pytest.raises(sav.OverMinError):
        sav.validate(User, "c4", 0)


def test_func12():
    assert sav.validate(User, "c4", 1) == 1


def test_func13():
    assert sav.validate(User, "c4", 3) == 3


def test_func14():
    with pytest.raises(sav.OverMaxError):
        sav.validate(User, "c4", 4)
