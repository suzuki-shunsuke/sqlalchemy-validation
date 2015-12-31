import sys
import os

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "convert_model_to_dict"
    id = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    c1 = sav.Column(sa.INTEGER)


def test_func1():
    user = User()
    assert sav.convert_model_to_dict(user) == {"id": None, "c1": None}
    assert sav.convert_model_to_dict(user, "id") == {"id": None}
    assert sav.convert_model_to_dict(user, id=3) == {"id": 3, "c1": None}
    assert sav.convert_model_to_dict(user, default_=3) == {"id": 3, "c1": 3}
    assert sav.convert_model_to_dict(user, remove_empty_=True) == {}
    assert sav.convert_model_to_dict(user, "id", c1=5) == {"id": None, "c1": 5}
    assert sav.convert_model_to_dict(user, "id", id=5) == {"id": 5}
    assert sav.convert_model_to_dict(user, "id", default_=5) == {"id": 5}
    assert sav.convert_model_to_dict(
        user, "id", remove_empty_=True
    ) == {}
    assert sav.convert_model_to_dict(
        user, id=3, default_=5
    ) == {"id": 3, "c1": 5}
    assert sav.convert_model_to_dict(
        user, id=3, remove_empty_=True
    ) == {"id": 3}
    assert sav.convert_model_to_dict(
        user, default_=3, remove_empty_=True
    ) == {"id": 3, "c1": 3}
    assert sav.convert_model_to_dict(
        user, "id", c1=3, default_=5
    ) == {"id": 5, "c1": 3}
    assert sav.convert_model_to_dict(
        user, "id", c1=3, remove_empty_=True
    ) == {"c1": 3}
    assert sav.convert_model_to_dict(
        user, "id", default_=3, remove_empty_=True
    ) == {"id": 3}
    assert sav.convert_model_to_dict(
        user, id=5, default_=3, remove_empty_=True
    ) == {"id": 5, "c1": 3}
    assert sav.convert_model_to_dict(
        user, "c1", id=5, default_=3, remove_empty_=True
    ) == {"id": 5, "c1": 3}
