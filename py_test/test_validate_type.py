import sys
import os
import datetime

import sqlalchemy as sa
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sqlalchemy_validation as sav

sys.path.pop()


class User(sav.Model):
    __tablename__ = "test_validate_type"
    integer = sav.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    boolean = sav.Column(sa.Boolean)
    date = sav.Column(sa.Date)
    datetime = sav.Column(sa.DateTime)
    enum = sav.Column(sa.Enum("foo", "bar"))
    float = sav.Column(sa.Float)
    interval = sav.Column(sa.Interval)
    string = sav.Column(sa.String)
    text = sav.Column(sa.Text)
    time = sav.Column(sa.Time)
    timestamp = sav.Column(sa.TIMESTAMP)


def test_integer1():
    assert sav.validate(User, "integer", 1) == 1


def test_integer2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "integer", "2")


def test_boolean1():
    assert sav.validate(User, "boolean", True) is True


def test_boolean2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "boolean", 1)


def test_date1():
    date = datetime.date.today()
    assert sav.validate(User, "date", date) == date


def test_date2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "date", 1)


def test_datetime1():
    datetime_ = datetime.datetime.today()
    assert sav.validate(User, "datetime", datetime_) == datetime_


def test_datetime2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "datetime", 1)


def test_enum1():
    assert sav.validate(User, "enum", "foo") == "foo"


def test_enum2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "enum", 1)


def test_float1():
    assert sav.validate(User, "float", 1.0) == 1.0


def test_float2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "float", 1)


def test_interval1():
    interval = datetime.timedelta(days=5)
    assert sav.validate(User, "interval", interval) == interval


def test_interval2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "interval", 1)


def test_string1():
    assert sav.validate(User, "string", "foo") == "foo"


def test_string2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "string", 1)


def test_text1():
    assert sav.validate(User, "text", "foo") == "foo"


def test_text2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "text", 1)


def test_time1():
    time = datetime.time(hour=5)
    assert sav.validate(User, "time", time) == time


def test_time2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "time", 1)


def test_timestamp1():
    timestamp = datetime.datetime.today()
    assert sav.validate(User, "timestamp", timestamp) == timestamp


def test_timestamp2():
    with pytest.raises(sav.InvalidTypeError):
        sav.validate(User, "timestamp", 1)
