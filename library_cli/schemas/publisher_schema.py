from marshmallow import fields, validates, ValidationError, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime
from library_cli.models import Publisher
from library_cli.static import Country


class PublisherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Publisher
        load_instance = True
        include_relationships = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    country = fields.Enum(enum=Country, required=True)
    founded_year = fields.Date(required=True)

    # Nested relationship
    books = fields.List(fields.Nested("BookSchema", exclude=("publisher",)), required=False)

    # Custom validation
    @validates("founded_year")
    def validate_founded_year(self, value, **kwargs):
        if value > datetime.now().date():
            raise ValidationError("founded_year cannot be in the future.")

    @validates("country")
    def validate_country(self, value, **kwargs):
        if value not in Country.__members__:
            raise ValidationError(f"Invalid country: {value}. Must be one of: {list(Country.__members__.keys())}")


Publisher.Schema = PublisherSchema
