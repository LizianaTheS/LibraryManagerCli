from marshmallow import fields, validates, ValidationError, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from library_cli.models.genres import Genre

from library_cli.models import Genre


class GenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        include_relationships = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=50))

    # Nested relationship
    books = fields.List(fields.Nested("BookSchema", exclude=("genres",)), required=False)

    # Custom validation
    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Genre name cannot be empty.")


Genre.Schema = GenreSchema
