import sqlalchemy as sa
from sqlalchemy_validation import Column
import pytest


def test_size():
    column = Column(sa.types.INTEGER, size=(10, 20))
