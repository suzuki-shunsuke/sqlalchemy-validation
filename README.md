# sqlalchemy-validation
SQLAlchemy Validation Extension.

## About

This library supports validations based on the model class definition by using the [Attribute Events](http://docs.sqlalchemy.org/en/latest/orm/events.html#attribute-events) .

Currently, this library supprts the following validations.

* Not Null Constraint
* Enum Constraint
* Type Constraint
* String Length Range Constraint
* RegExp Constraint
* Email Constraint
* Size Constraint

These validations don't have to the database connection,
and you don't have to execute explicitly.

## Example

```python
import re
import datetime

import sqlalchemy as sa
from sqlalchemy_validation import Model, Column


class Person(Model):
    __tablename__ = 'person'
    id = Column(sa.Integer, primary_key=True)
    name = Column(sa.VARCHAR(20), length=(None, 15), unique=True, regexp=re.compile(r'[a-z0-9]*'))
    age = Column(sa.Integer, size=(20, 40))
    birth = Column(sa.DateTime, size=(None, datetime.now()), nullable=False)
    email = Column(sa.VARCHAR(20), format='email')  # require validate_email


try:
    person = Person(id='foo')
except ValidationError as errors:
    for column_names, error in errors.items():
        print(column_names)  # ("id",)
        assert isinstance(error, InvalidTypeError)

person = Person()
try:
    person.age = 10
except SizeError as e:
    person.age  # None
    e.value  # 10
```

## Dependencies

* Python 3
* SQLAlchemy
* [validate_email](https://pypi.python.org/pypi/validate_email)(optional)

If you verify if email is valid, install validate_email.

## Install

```
$ pip install sqlalchemy_validation
```


## License

This Library is distributed under the [MIT license](LICENSE).
