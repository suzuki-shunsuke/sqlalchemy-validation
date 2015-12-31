import sys
import os

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "validate_email"
    id = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    c1 = sav.Column(sa.VARCHAR(20), format="email")


def test_func1():
    assert sav.validate(User, "c1", "foo@gmail.com") == "foo@gmail.com"


def test_func2():
    with pytest.raises(sav.EmailError):
        sav.validate(User, "c1", "1")
