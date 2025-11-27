# decorators.py
from functools import wraps
from .session_manager import SessionManager

def with_session(func):
    """Inject session automatically into instance method."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        sm = SessionManager()
        with sm.session_scope() as session:
            return func(self, session, *args, **kwargs)
    return wrapper

def class_session(func):
    """Inject session automatically into class method."""
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        sm = SessionManager()
        with sm.session_scope() as session:
            return func(cls, session, *args, **kwargs)
    return wrapper
