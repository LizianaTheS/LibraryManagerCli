from ..utils.common_decorators import check_class_arguments
from .decorator import with_session, class_session
from library_cli.config.logging import get_logger

logger = get_logger(__name__)


class BaseMixin:
    """Class-level operations"""

    @classmethod
    @check_class_arguments
    @class_session
    def create(cls, session ,**fields):
        obj = cls(**fields)
        session.add(obj)
        session.flush()
        session.refresh(obj)
        logger.info("Created %s(id=%s)", cls.__name__, obj.id)
        return obj

    @classmethod
    @class_session
    def get(cls, session, id: int):
        obj = session.get(cls, id)
        if obj:
            logger.info("Fetched %s(id=%s)", cls.__name__, obj.id)
        else:
            logger.warning("No %s found with id=%s", cls.__name__, id)
        return obj


class InstanceMixin:
    """Instance-level operations (delete/update on the object itself)"""

    @with_session
    def delete(self, session):
        session.delete(self)
        logger.info("Deleted %s(id=%s)", self.__class__.__name__, self.id)

    @with_session
    @check_class_arguments
    def update(self, session, **fields):
        for key, value in fields.items():
            setattr(self, key, value)
        session.flush()
        session.refresh(self)
        logger.info("Updated %s(id=%s)", self.__class__.__name__, self.id)


class BatchMixin:
    """For batch operations in one transaction"""

    @classmethod
    def batch(cls, func):
        """Run multiple operations in one session"""
        from .session_manager import SessionManager
        sm = SessionManager()
        with sm.session_scope() as session:
            return func(session)
