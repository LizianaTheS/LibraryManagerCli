from sqlalchemy.orm import Session
from contextlib import contextmanager
from library_cli.config.logging import get_logger
from library_cli.config.sqlalchemy import SessionLocal

logger = get_logger(__name__)



class SessionManager:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    @contextmanager
    def session_scope(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.exception("Session rollback due to: %s", e)
            raise
        finally:
            session.close()

    def get_session(self):
        """Return a session for manual handling if needed"""
        return self.session_factory()
