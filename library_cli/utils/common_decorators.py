from functools import wraps


def check_class_arguments(func):
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        valid_columns = valid_columns = set(cls.__mapper__.c.keys()) | set(
            cls.__mapper__.relationships.keys()
        )

        invalid_columns = {"id"}
        for key in kwargs:
            if key not in valid_columns or key in invalid_columns:
                raise AttributeError(f"{cls.__name__} has no column '{key}'")
        return func(cls, *args, **kwargs)

    return wrapper