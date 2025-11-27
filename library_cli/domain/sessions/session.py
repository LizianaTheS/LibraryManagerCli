class SessionManager:
    _current_member = None

    @classmethod
    def login(cls, member):
        cls._current_member = member

    @classmethod
    def logout(cls):
        cls._current_member = None

    @classmethod
    def current(cls):
        return cls._current_member

    @classmethod
    def is_authenticated(cls):
        return cls._current_member is not None

    @classmethod
    def get_user(cls):
        return cls._current_member
