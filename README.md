# sqlalchemy-validation
SQLAlchemy Validation Extension.

## About

This library supports the validation based on the model class definition.

This library supports two type validations.

* validation using the [validates](http://docs.sqlalchemy.org/en/improve_toc/orm/mapped_attributes.html?highlight=validate#sqlalchemy.orm.validates) decorator
* validation using model's validate_insert method

### validation using the validates decorator

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

### validation using model's validate_insert method

Currently, this library supprts the following validations.

* Primary Key Constraint
* Unique Constraint

These validations have to the database connection,
and you have to execute explicitly.

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

person = Person(id='foo')  # raise InvalidTypeError
person = Person(name='a' * 20)  # raise TooLongError
person = Person(name='---')  # raise RegExpError
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
