from sqlalchemy.orm import Session

from library_cli.config.logging import get_logger
from library_cli.models import Genre
from library_cli.schemas import GenreSchema


class GenreService:
    def __init__(self, session: Session):
        self.session = session
        self.logger = get_logger(self.__class__.__name__)
        self.schema = GenreSchema
        self._model = Genre

    def get_schema(self, load_instance: bool = True):
        return self.schema(load_instance=load_instance, session=self.session)

    def create(self, name: str):
        existing = self.session.query(Genre).filter(Genre.name == name).first()
        if existing:
            raise ValueError(f"You already have a genre named {name}")
        schema = self.get_schema()
        genre = schema.load({"name": name}, session=self.session)
        self.session.add(genre)
        # log here
        return genre

    def get(self, genre_id: int, dumped: bool = False):
        schema = self.get_schema()
        genre = self.session.get(Genre, genre_id)
        if not genre:
            # log here
            raise ValueError(f"No genre found with id {genre_id}")
        return schema.dump(genre) if dumped else genre

    def update(self, genre_id: int, name: str):
        genre = self.get(genre_id)
        schema = self.get_schema()
        new = schema.load({"name": name}, session=self.session, instance=genre)
        self.session.add(new)
        return new

    def delete(self, genre_id: int):
        genre = self.get(genre_id)
        self.session.delete(genre)

    def get_all_genres(self, dumped: bool = False):
        schema = self.get_schema()
        genres = self.session.query(Genre).all()
        return schema.dump(genres, many=True) if dumped else genres
