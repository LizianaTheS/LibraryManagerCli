from marshmallow import fields, validates, ValidationError, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from library_cli.models import Author
from library_cli.static import Country


class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True
        include_relationships = True  # include books

    # Fields with explicit validation
    id = fields.Int(dump_only=True)
    fullname = fields.Str(required=True, validate=validate.Length(max=100))
    birth_year = fields.Date(required=True)
    death_year = fields.Date(allow_none=True)
    # nationality = fields.Str(required=True)
    nationality = fields.Enum(Country, required=True)

    # Nested relationship
    books = fields.List(fields.Nested("BookSchema", exclude=("authors",)), required=False)

    # Custom validation
    @validates("birth_year")
    def validate_birth_year(self, value, **kwargs):
        from datetime import datetime
        if value > datetime.now().date():
            raise ValidationError("birth_year cannot be in the future.")

    @validates("death_year")
    def validate_death_year(self, value, **kwargs):
        from datetime import datetime
        if value and value > datetime.now().date():
            raise ValidationError("death_year cannot be in the future.")

    # @validates("nationality")
    # def validate_nationality(self, value, **kwargs):
    #     if value not in Country.__members__:
    #         raise ValidationError(f"{value} is not a valid Country.")
    @validates("nationality")
    def validate_nationality(self, value, **kwargs):
        if not isinstance(value, Country):
            raise ValidationError(f"{value} is not a valid Country.")


Author.Schema = AuthorSchema
