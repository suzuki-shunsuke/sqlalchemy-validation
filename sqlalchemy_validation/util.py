"""
"""


def validate(Model, *args, **kwargs):
    """ Validate values.
    The validates function raises ValidtionError,
    while the validate function raises ValidatesError.

    If you want to know only if kwargs are valid or not,
    you should use the validate function rather than the validates function
    in terms of the efficiency.

    If you validate only one pair of column name and value,
    you can use positional arguments.

    If you pass positional arguments, keyword arguments are ignored.

    Args:
      Model: A model class.
      *args: a column name and value.
      **kwargs: pairs of the column name and value.

    Returns:
      If you pass positional arguments,
      keyword arguments are ignored and the value is returned.
      If you pass keyword arguments, return a model instance.

    Raises:
      ValidatesError
    """
    model = Model()
    if len(args) >= 2:
        column_name, value = args[:2]
        setattr(model, column_name, value)
        return getattr(model, column_name)
    for column_name, value in kwargs.items():
        setattr(model, column_name, value)
    return model


def validates(Model, **kwargs):
    """ Validate values.

    Args:
      Model: A model class.
      **kwargs: pairs of the column name and value.

    Returns:
      A model.

    Raises:
      ValidationError
    """
    return Model(**kwargs)


def convert_model_to_dict(model, *args, **kwargs):
    """ Convert a model instance to a dict object.

    Args:
      model: a model instance.
      *args: extracted column names.
      **kwargs:
        kwargs[column_name]: column's default value.
          This takes preference over the default_ keyword.
        default_: default value
        remove_empty_:
          If this is True, empty columns are ignored.
          If the default value is set, this is ignored.
          This default value is False.

    Returns:
      A dict object.

    Examples:
      user = User()
      convert_model_to_dict(user)  # {"id": None, "name": None, "age": None}
      convert_model_to_dict(user, "name")  # {"name": None}
      # {"id": None, "name": "foo", "age": None}
      convert_model_to_dict(user, name="foo")
      # {"id": "foo", "name": "foo", "age": "foo"}
      convert_model_to_dict(user, default_="foo")
      convert_model_to_dict(user, remove_empty_=True)  # {}
      convert_model_to_dict(user, "name", id=1)  # {"id": 1, "name": None}
      convert_model_to_dict(user, "name", name="bar")  # {"name": "bar"}
      convert_model_to_dict(user, "name", default_="foo")  # {"name": "foo"}
      convert_model_to_dict(user, "name", remove_empty_=True)  # {}
      # {"id": "bar", "name": "foo", "age": "bar"}
      convert_model_to_dict(user, name="foo", default_="bar")
      # {"name": "foo"}
      convert_model_to_dict(user, name="foo", remove_empty_=True)
      # {"id": "foo", "name": "foo", "age": "foo"}
      convert_model_to_dict(user, default_="foo", remove_empty_=True)
      # {"id": 1, "name": "foo"}
      convert_model_to_dict(user, "name", id=1, default_="foo")
      # {"id": 1}
      convert_model_to_dict(user, "name", id=1, remove_empty_=True)
      # {"id": 1, "name": "foo", "age": "foo"}
      convert_model_to_dict(user, id=1, default_="foo", remove_empty_=True)
      # {"id": 1, "name": "foo"}
      convert_model_to_dict(user, "name", id=1, default_="foo",
                            remove_empty_=True)
    """
    remove_empty = kwargs.pop("remove_empty_", False)
    has_default = "default_" in kwargs
    default = kwargs.pop("default_", None)
    column_names = model.__table__.c.keys()
    model_vars = vars(model)

    if has_default:
        # ignore remove_empty
        if args:
            ret = dict((key, model_vars.get(key, default))
                       for key in args)
            for key, val in kwargs.items():
                ret[key] = model_vars.get(key, val)
            return ret
        else:
            return dict((key, model_vars.get(key, kwargs.get(key, default)))
                        for key in column_names)
    else:
        if remove_empty:
            if args:
                ret = dict((key, model_vars[key])
                           for key in args if key in model_vars)
                for key, val in kwargs.items():
                    ret[key] = model_vars.get(key, val)
                return ret
            else:
                ret = dict(model_vars)
                ret.pop("_sa_instance_state")
                for key, val in kwargs.items():
                    ret[key] = ret.get(key, val)
                return ret
        else:
            if args:
                ret = dict(kwargs)
                for key in args:
                    ret[key] = model_vars.get(key, ret.get(key, default))
                return ret
            else:
                return dict(
                    (key, model_vars.get(key, kwargs.get(key, default)))
                    for key in column_names
                )
