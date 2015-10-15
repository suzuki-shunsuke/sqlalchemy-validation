"""
SQLAlchemy Validation

Example:

from sqlalchemy_validation import Model, Column

class User(Base):
    __tablename__ = "users"
    name = Column(mysql.VARCHAR(20), primary_key=True,
                  regexp=re.compile(r"[-._0-9a-z]{4,10}"))
    email = Column(mysql.VARCHAR(50), nullable=False, unique=True)
    age = Column(mysql.INTEGER, default=20, nullable=False)
    status = Column(mysql.ENUM("active", "leaved"), nullable=False)
"""

from .model import Model
from .column import Column
from .error import *
