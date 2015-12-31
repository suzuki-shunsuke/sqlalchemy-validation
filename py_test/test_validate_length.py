import sys
import os

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "validate_legnth"
    id = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    c1 = sav.Column(sa.VARCHAR(5))
    c2 = sav.Column(sa.VARCHAR(5), length=(None, 3))
    c3 = sav.Column(sa.VARCHAR(5), length=(1, None))
    c4 = sav.Column(sa.VARCHAR(5), length=(1, 3))


def test_func1():
    assert sav.validate(User, "c1", "") == ""


def test_func2():
    assert sav.validate(User, "c1", "12345") == "12345"


def test_func3():
    with pytest.raises(sav.TooLongError):
        sav.validate(User, "c1", "123456")


def test_func4():
    assert sav.validate(User, "c2", "") == ""


def test_func5():
    assert sav.validate(User, "c2", "123") == "123"


def test_func6():
    with pytest.raises(sav.TooLongError):
        sav.validate(User, "c2", "1234")


def test_func7():
    with pytest.raises(sav.TooShortError):
        sav.validate(User, "c3", "")


def test_func8():
    assert sav.validate(User, "c3", "1") == "1"


def test_func9():
    assert sav.validate(User, "c3", "12345") == "12345"


def test_func10():
    with pytest.raises(sav.TooLongError):
        sav.validate(User, "c3", "123456")


def test_func11():
    with pytest.raises(sav.TooShortError):
        sav.validate(User, "c4", "")


def test_func12():
    assert sav.validate(User, "c4", "1") == "1"


def test_func13():
    assert sav.validate(User, "c4", "123") == "123"


def test_func14():
    with pytest.raises(sav.TooLongError):
        sav.validate(User, "c4", "1234")
