from psycopg.generators import fetch
from sqlalchemy.orm import Session

from library_cli.config.logging import get_logger
from library_cli.models import Reservation
from library_cli.schemas import ReservationSchema
from datetime import datetime, timedelta

from library_cli.static import Status
from library_cli.utils.helper_func import to_enum


class ReservationService:
    def __init__(self, session: Session):
        self.session = session
        self.schema = ReservationSchema
        self._model = Reservation
        self.logger = get_logger(self.__class__.__name__)

    def get_schema(self, load_instance: bool = True):
        return self.schema()

    def reserve(self, copy: "Copy", member: "Member"):
        schema = self.get_schema()

        existing = self.session.query(Reservation).filter(
            Reservation.reserved_at.isnot(None),
            Reservation.copy_id == copy.id,
            Reservation.member_id == member.id,
            Reservation.status == Status.ACTIVE,
            Reservation.expires_at > datetime.now()
        ).first()

        if existing:
            raise ValueError(f"You already reserved this copy in {existing.reserved_at}")

        raw_data = {
            "copy_id": copy.id,
            "member_id": member.id,
            "reserved_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(days=2),
            "status": "ACTIVE"
        }

        _data = schema.load(raw_data)

        reservation = Reservation(
            copy_id=_data["copy_id"],
            member_id=_data["member_id"],
            reserved_at=_data["reserved_at"],
            expires_at=_data["expires_at"],
            status=to_enum(Status, _data["status"]),
            member=member,
            copy=copy
        )

        self.session.add(reservation)
        return reservation

    def get(self, reservation_id: int, dumped: bool = False):
        reservation = self.session.get(Reservation, reservation_id)
        schema = self.get_schema()
        if not reservation:
            # log
            raise ValueError(f"No reservation found with id {reservation_id}")
        return reservation if dumped == False else schema.dump(reservation)

    def cancel_reservation(self, reservation_id: int):
        reservation = self.get(reservation_id)
        self.session.delete(reservation)

    def get_x_reservation(self, copy_id: int, member_id: int, reserved: bool = None, expired: bool = None,
                          status: str = None,
                          dumped: bool = False, many: bool = None):
        schema = self.get_schema()
        query = self.session.query(Reservation)
        filters = [Reservation.copy_id == copy_id, Reservation.member_id == member_id]
        if reserved is True:
            filters.append(Reservation.reserved_at.isnot(None))
        elif reserved is False:
            filters.append(Reservation.reserved_at.is_(None))
        if expired is True:
            filters.append(Reservation.expires_at < datetime.now())
        elif expired is False:
            filters.append(Reservation.expires_at >= datetime.now())
        if status:
            filters.append(Reservation.status == to_enum(Status, status))
        query = query.filter(*filters)

        fetched = query.all() if many else query.first()

        return schema.dump(fetched, many=many) if dumped else fetched

    def get_all(self, reserved: bool = None, expired: bool = None,
                status: str = None,
                dumped: bool = False, many: bool = None):
        schema = self.get_schema()
        query = self.session.query(Reservation)
        filters = []
        if reserved is True:
            filters.append(Reservation.reserved_at.isnot(None))
        elif reserved is False:
            filters.append(Reservation.reserved_at.is_(None))
        if expired is True:
            filters.append(Reservation.expires_at < datetime.now())
        elif expired is False:
            filters.append(Reservation.expires_at >= datetime.now())
        if status:
            filters.append(Reservation.status == to_enum(Status, status))
        query = query.filter(*filters)
        fetched = query.all() if many else query.first()
        return schema.dump(fetched, many=many) if dumped else fetched
