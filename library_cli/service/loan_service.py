from sqlalchemy.orm import Session

from library_cli.models import Loan
from library_cli.schemas import LoanSchema
from library_cli.config.logging import get_logger
from datetime import datetime

from library_cli.static import Action


class LoanService:
    def __init__(self, session: Session):
        self.logger = get_logger(self.__class__.__name__)
        self.session = session
        self.schema = LoanSchema
        self._model = Loan

    def get_schema(self):
        return self.schema()

    def borrow_copy(self, copy: "Copy", member: "Member"):
        active_loan = (
            self.session.query(Loan)
            .filter(Loan.copy_id == copy.id, Loan.returned_at.is_(None))
            .first()
        )
        if active_loan:
            raise ValueError("Copy already borrowed.")

        schema = self.get_schema()

        load_data = {
            "copy_id": copy.id,
            "member_id": member.id,
            "borrowed_at": datetime.now(),
        }

        _data = schema.load(load_data)

        loan = Loan(copy_id=_data["copy_id"], copy=copy, member_id=_data["member_id"], member=member,
                    borrowed_at=_data["borrowed_at"], returned_at=None)

        self.session.add(loan)

        copy.action = Action.BORROWED

        return loan

    def return_copy(self, copy: "Copy"):
        active_loan = self.session.query(Loan).filter(Loan.copy_id == copy.id, Loan.returned_at.is_(None)).first()
        if not active_loan:
            # log here
            raise ValueError(f"Copy doesn't need to return and is already {copy.action}")

        active_loan.returned_at = datetime.now()
        copy.action = Action.FREE

        return active_loan

    def get_x_loan(self, borrowed_at: bool = None, returned_at: bool = None, many: bool = False):
        query = self.session.query(Loan)
        filters = []

        if borrowed_at is True:
            filters.append(Loan.borrowed_at.isnot(None))
        elif borrowed_at is False:
            filters.append(Loan.borrowed_at.is_(None))

        if returned_at is True:
            filters.append(Loan.returned_at.isnot(None))
        elif returned_at is False:
            filters.append(Loan.returned_at.is_(None))

        query = query.filter(*filters)

        return query.all() if many else query.first()
