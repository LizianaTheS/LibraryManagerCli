# from marshmallow import fields, validates, ValidationError, validate, post_load
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields, validates, ValidationError
# from library_cli.models.book import Book
from library_cli.static import Language
from library_cli.models import Book


# Lazy import to avoid circular references


class BookSchema(Schema):
    title = fields.Str(required=True)
    subtitle = fields.Str(allow_none=True)
    isbn = fields.Str(allow_none=True)
    edition = fields.Str(allow_none=True)
    pages = fields.Int(allow_none=True)
    language = fields.Enum(Language, required=True)
    published_year = fields.Date(required=True)
    genre_id = fields.Int(required=True)
    publisher_id = fields.Int(required=True)

    # Custom validation

    @validates("published_year")
    def validate_published_year(self, value, **kwargs):
        from datetime import datetime
        if value and value > datetime.now().date():
            raise ValidationError("published_year cannot be in the future.")

    @validates("language")
    def validate_language(self, value, **kwargs):
        if value not in Language.__members__:
            raise ValidationError(f"Invalid language: {value}. Must be one of: {list(Language.__members__.keys())}")


Book.Schema = BookSchema
