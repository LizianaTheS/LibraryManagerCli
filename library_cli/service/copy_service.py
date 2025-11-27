from typing import List

from sqlalchemy.orm import Session, joinedload

from library_cli.static import Condition, Action
from library_cli.utils.helper_func import generate_barcode, to_enum
from library_cli.config.logging import get_logger
from library_cli.models import Copy
from library_cli.schemas.copy_schema import CopySchema


class CopyService:
    def __init__(self, session: Session):
        self.logger = get_logger(self.__class__.__name__)
        self._model = Copy
        self.schema = CopySchema
        self.session = session

    def get_schema(self, load_instance: bool = True):
        return self.schema()

    def create(self, book: "Book", data: dict):
        schema = self.get_schema()
        barcode = generate_barcode()
        load_data = {
            "barcode": barcode,
            "action": "FREE",
            "condition": "GOOD",
            "book_id": book.id
        }
        load_data.update(data)
        _data = schema.load(load_data)
        action_enum = to_enum(Action, _data["action"])
        condition_enum = to_enum(Condition, _data["condition"])
        copy = Copy(book.id, barcode, book, condition_enum,
                    action_enum)
        self.session.add(copy)
        self.logger.info("Copy `%s` added to the database.", copy.book.title)
        return copy

    def get(self, copy_id: int, dumped: bool = False):
        copy = self.session.get(Copy, copy_id)
        if not copy:
            self.logger.warning("Warning: Not Found, Class: Copy, Message: No copy found with id %s", copy_id)
            raise ValueError(f"No copy found with id {copy_id}")
        return copy if not dumped else self.get_schema().dump(copy)

    def mark_condition_as(self, condition: str, copy_id: int) -> Copy:
        copy = self.get(copy_id)
        copy.condition = to_enum(Condition, condition)
        return copy

    def mark_action_as(self, action: str, copy_id: int) -> Copy:
        copy = self.get(copy_id)
        copy.action = to_enum(Action, action)
        return copy

    def get_x_copy(self, action: str = None, condition: str = None, many: bool = False, dumped: bool = False):
        query = self.session.query(Copy)
        schema = self.get_schema()
        fetched = None
        filters = []

        if action:
            filters.append(Copy.action == to_enum(Action, action))
        if condition:
            filters.append(Copy.condition == to_enum(Condition, condition))
        mid_query = query.filter(*filters)
        if many:
            fetched = mid_query.all()
        else:
            fetched = mid_query.first()

        if not dumped:
            return fetched

        if many:
            return schema.dump(fetched or [], many=True)
        else:
            return schema.dump(fetched, many=False)

    def get_loans(self, copy_id: int) -> List["Loan"]:
        copy = self.session.query(Copy).options(joinedload(Copy.loans)).filter(Copy.id == copy_id).first()
        if not copy:
            self.logger.warning("Warning: Not Found, Class: Copy, Message: No copy found with id %s", copy_id)
            raise ValueError(f"No copy found with id {copy_id}")
        return copy.loans

    def get_reservations(self, copy_id: int) -> List["Reservation"]:
        copy = self.session.query(Copy).options(joinedload(Copy.reservations)).filter(Copy.id == copy_id).first()
        if not copy:
            self.logger.warning("Warning: Not Found, Class: Copy, Message: No copy found with id %s", copy_id)
            raise ValueError(f"No copy found with id {copy_id}")
        return copy.reservations

    def get_all_copies(self, dumped: bool = False):
        schema = self.get_schema()
        copies = self.session.query(Copy).all()
        return schema.dump(copies, many=True) if dumped else copies
