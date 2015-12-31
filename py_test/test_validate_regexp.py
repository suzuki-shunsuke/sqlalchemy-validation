import sys
import os
import re

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "validate_regexp"
    id = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    c1 = sav.Column(sa.VARCHAR(10), regexp=re.compile(r"^test"))


def test_func1():
    assert sav.validate(User, "c1", "test1") == "test1"


def test_func2():
    with pytest.raises(sav.RegExpError):
        sav.validate(User, "c1", "1")
