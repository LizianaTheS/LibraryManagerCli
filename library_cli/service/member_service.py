# SQLALCHEMY imports
from sqlalchemy.orm import Session, selectinload, joinedload
# LOCAL PROJECT imports
from library_cli.domain.security.pass_manager import PasswordManager
from library_cli.domain.sessions.session import SessionManager
from library_cli.schemas.member_schema import MemberSchema
from library_cli.config.logging import get_logger
from library_cli.models.member import Member
from library_cli.static import Status
# LIBRARY imports
from typing import List, Dict
from datetime import datetime

from library_cli.utils.helper_func import to_enum


class MemberService:
    def __init__(self, session: Session):
        self.schema = MemberSchema
        self.pass_manager = PasswordManager()
        self.session_manager = SessionManager()
        self.logger = get_logger(self.__class__.__name__)
        self._model = Member
        self.session = session

    # -----------------------------
    # Basic CRUD
    # -----------------------------

    def get_schema(self, load_instance: bool = True):
        return self.schema()

    def create(self, data: dict) -> Member:
        """
        Create a new library members in the system.

        This method validates the input data, checks for existing members
        with the same username or email, hashes the password, and
        creates a new Member record in the database.

        Args:
            data (dict or Dict[str, str]): Dictionary containing members information. Required keys:
                - "fullname": Full name of the members (str)
                - "username": Unique username (str)
                - "email": Email address (str)
                - "password": Plain-text password (str)

        Raises:
            ValueError: If a members with the same username or email already exists.

        Returns:
            Member: The newly created Member instance.

        Example:
            \>>> member_service.create({
            ...     "fullname": "John Doe",
            ...     "username": "jdoe",
            ...     "email": "jdoe@example.com",
            ...     "password": "secret"
            ... })
            <Member id=1 username='jdoe'>
        """
        schema = self.get_schema()

        # Validate input first
        _data = schema.load(data)

        # Convert status string to enum
        status_enum = to_enum(Status, _data["status"])

        # Check username/email uniqueness
        if self.session.query(
                self.session.query(self._model).filter(self._model.username == _data["username"]).exists()
        ).scalar():
            raise ValueError(f"Username `{_data['username']}` already exists.")

        if self.session.query(
                self.session.query(self._model).filter(self._model.email == _data["email"]).exists()
        ).scalar():
            raise ValueError(f"Email `{_data['email']}` already exists.")

        # Hash password
        hashed_password = self.pass_manager.hash(_data["password"])

        member = Member(
            fullname=_data["fullname"],
            email=_data["email"],
            username=_data["username"],
            password=hashed_password,
            status=status_enum
        )

        self.session.add(member)
        return member

    def update(self, member_id: int, data: dict) -> Member:
        """
        Update an existing library members's information in the system.

        This method retrieves a Member record by its ID, validates the input data,
        applies updates to the members's attributes, and commits the changes to the database.
        Only fields provided in the `data` dictionary will be updated.

        Args:
            member_id (int): The unique identifier of the members to update.
            data (Dict[str, Any]): Dictionary containing the fields to update. Possible keys include:
                - "fullname" (str): Full name of the members.
                - "username" (str): Unique username.
                - "email" (str): Email address.
                - "password" (str): Plain-text password (will be hashed before saving).

        Raises:
            ValueError: If no members with the given ID exists, or if the updated username/email
                        conflicts with another members.

        Returns:
            Member: The updated Member instance with the applied changes.
        """
        self.logger.info(f"Attempting to update Member(id={member_id}) with data: {data}")

        # Fetch the member
        member = self.get(member_id=member_id)
        if not member:
            raise ValueError(f"Member with id={member_id} not found")

        # Load and validate data (partial=True allows updating only some fields)
        schema = self.get_schema()
        validated_data = schema.load(data, partial=True)

        # Handle status conversion if present
        if "status" in validated_data:
            validated_data["status"] = to_enum(Status, validated_data["status"])

        # Update the member fields dynamically
        for key, value in validated_data.items():
            setattr(member, key, value)

        # Add to session and commit (or session scope will handle commit)
        self.session.add(member)
        self.logger.info(
            "Member updated successfully: id=%s, username=%s, email=%s",
            member.id, member.username, member.email
        )
        return member

    def get(self, member_id: int, dumped: bool = False) -> Member:
        schema = self.get_schema()
        member = self.session.get(Member, member_id)
        if not member:
            self.logger.warning(f"Member(id={id}) not found. Operation aborted.")
            raise ValueError(f"Member `{id}` not found")
        return member if not dumped else schema.dump(member)

    def delete(self, member_id: int) -> None:
        member = self.get(member_id=member_id)
        self.session.delete(member)
        self.logger.warning(f"Member(id={member_id}) has been deleted. Operation succeed.")

    # -----------------------------
    # Lookup / Queries
    # -----------------------------

    def filter_query(self, session: Session, **kwargs):
        return session.query(self._model).filter_by(**kwargs)

    def query(self, session: Session):
        return session.query(self._model)

    def search_member(self, fullname: str = None, phone: str = None) -> List[Member]:
        schema = self.get_schema(False)
        _data = schema.load({"fullname": fullname, "phone": phone}, partial=True)

        query = self.session.query(Member)
        filters = []

        name = _data.get("fullname")
        if name:
            filters.append(Member.fullname.ilike(f"%{name}%"))

        ph = _data.get("phone")
        if ph:
            filters.append(Member.phone.ilike(f"%{ph}%"))

        if filters:
            query = query.filter(*filters)

        return query.all()

    # -----------------------------
    # Status / Activity
    # -----------------------------

    def mark_status_as(self, status: Status, member_id: int) -> Member:
        member = self.get(member_id)
        member.status = status
        self.logger.warning(f"Member(member_id={member_id}) status has been changed to {status}. Operation succeed.")
        return member

    def is_member_status_x(self, member_id: int, status: Status):
        member = self.get(member_id)
        return member.status == status

    # -----------------------------
    # Member Resources
    # -----------------------------

    def get_members(self, dumped: bool = False):
        schema = self.get_schema()
        members = (self.session.query(self._model)
                   .options(
            joinedload(Member.logs),
            joinedload(Member.loans),
            joinedload(Member.reservations)
        ).all())
        return schema.dumps(members, many=True) if dumped else members

    def get_loans(self, member_id: int) -> List["Loan"]:
        member = self.session.query(Member).options(selectinload(Member.loans)).get(id)
        if not member:
            self.logger.warning(f"Member(id={member_id}) not found. Operation aborted.")
            raise ValueError(f"Member `{member_id}` not found")
        return member.loans

    def get_reservations(self, member_id: int) -> List["Reservation"]:
        member = self.session.query(Member).options(selectinload(Member.reservations)).get(id)
        if not member:
            self.logger.warning(f"Member(id={member_id}) not found. Operation aborted.")
            raise ValueError(f"Member `{member_id}` not found")
        return member.reservations

    def get_active_reservations(self, member_id: int) -> List["Reservation"]:
        member = self.session.query(Member) \
            .options(selectinload(Member.reservations)) \
            .get(id)

        if not member:
            self.logger.warning(f"Member(id={member_id}) not found. Operation aborted.")
            raise ValueError(f"Member `{member_id}` not found")

        active_reservations = [
            r for r in member.reservations
            if r.status == Status.ACTIVE and r.expires_at > datetime.now
        ]
        return active_reservations

    def get_active_loans(self, member_id: int) -> List["Loan"]:
        member = self.session.query(Member) \
            .options(selectinload(Member.loans)) \
            .get(member_id)

        if not member:
            self.logger.warning(f"Member(id={member_id}) not found. Operation aborted.")
            raise ValueError(f"Member `{member_id}` not found")

        active_loans = [
            l for l in member.loans
            if l.returned_at is None
        ]
        return active_loans

    # -----------------------------
    # Authentication / Security
    # -----------------------------
    def update_password(self, member_id: int, old_pass: str, new_pass: str):
        member = self.get(member_id)
        if not member:
            self.logger.warning(f"Member(id={member_id}) not found. Operation aborted.")
            raise ValueError("Member not found")

        if self.pass_manager.verify(old_pass, str(member.password)):
            member.password = self.pass_manager.hash(new_pass)
            self.logger.info("member password has been updated successfully")
        else:
            self.logger.info("member entered wrong password")
            raise ValueError("Wrong password.")

    def login(self, username: str, password: str):
        """
        Authenticate a member using their username and password.

        Parameters
        ----------
        session : Session
            The SQLAlchemy session provided by the `with_session` decorator.
        username : str
            The username of the member attempting to log in.
        password : str
            The plaintext password to verify against the stored hash.

        Returns
        -------
        Member
            The authenticated member object if verification succeeds.

        Raises
        ------
        ValueError
            If no member exists with the given username.
            If the provided password does not match the stored password hash.

        Notes
        -----
        This method performs three steps:
        1. Look up the member by username.
        2. Verify the provided password using the password manager.
        3. Register the successful login using the session manager.

        The `with_session` decorator ensures that session lifecycle
        management (commit/rollback/cleanup) is handled externally.
        """
        schema = self.get_schema()
        _data = schema.load({"username": username, "password": password}, session=self.session, partial=True)
        member = self.session.query(Member).filter(Member.username == _data.username).first()

        if not member:
            self.logger.warning(f"Member(id={member.id}) not found. Operation aborted.")
            raise ValueError("Member not found")

        if self.pass_manager.verify(_data.password, str(member.password)):
            self.session_manager.login(member)
            return member

        raise ValueError("wrong password")

    def logout(self):
        member = self.session_manager.current()
        if not member:
            raise ValueError("You need to login first.")
        self.session_manager.logout()
