from typing import List

from sqlalchemy.orm import Session

from library_cli.models import Publisher
from library_cli.schemas import PublisherSchema
from library_cli.config.logging import get_logger
from datetime import date, datetime

from library_cli.static import Country
from library_cli.utils.helper_func import to_enum


class PublisherService:
    def __init__(self, session: Session):
        self.logger = get_logger(self.__class__.__name__)
        self.session = session
        self.schema = PublisherSchema
        self._model = Publisher

    def get_schema(self, load_instance: bool = True):
        return self.schema(load_instance=load_instance, session=self.session)

    def create(self, name: str, country: str, founded_year: str):
        existing = self.session.query(Publisher).filter(
            Publisher.name == name,
            Publisher.country == country
        ).first()
        if existing:
            # log here
            raise ValueError("You already have a publisher with same name and country")

        schema = self.get_schema()
        fy = datetime.strptime(founded_year, "%Y-%m-%d").date()
        publisher = schema.load(
            data={"name": name, "country": to_enum(Country, country), "founded_year": fy},
            session=self.session)
        self.session.add(publisher)
        return publisher

    def get(self, publisher_id: int, dumped: bool = False):
        schema = self.get_schema()
        publisher = self.session.get(Publisher, publisher_id)
        if not publisher:
            # log here
            raise ValueError(f"No publisher found with id {publisher_id}")
        return schema.dump(publisher) if dumped else publisher

    def update(self, publisher_id: int, name: str, country: str, founded_year: str):
        publisher = self.get(publisher_id)
        schema = self.get_schema()
        new = schema.load(
            data={"name": name, "country": to_enum(Country, country),
                  "founded_year": datetime.strptime(founded_year, "%Y-%m-%d").date()},
            session=self.session,
            instance=publisher)
        self.session.add(new)
        return new

    def delete(self, publisher_id: int):
        publisher = self.get(publisher_id)
        self.session.delete(publisher)

    def get_all(self, dumped: bool = False) -> List[Publisher]:
        schema = self.get_schema()
        publishers = self.session.query(Publisher).all()
        return schema.dump(publishers, many=True) if dumped else publishers
