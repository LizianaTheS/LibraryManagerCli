from marshmallow import fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from library_cli.static import Action
from library_cli.models import InventoryLog


# Lazy imports for circular references


class InventoryLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InventoryLog
        load_instance = True
        include_relationships = True

    id = fields.Int(dump_only=True)
    action = fields.Enum(Action, required=True)
    book = fields.Nested("BookSchema", exclude=("logs",), required=True)
    member = fields.Nested("MemberSchema", exclude=("logs",), required=True)

    # Validation
    @validates("action")
    def validate_action(self, value, **kwargs):
        if value not in Action.__members__:
            raise ValidationError(f"Invalid action: {value}. Must be one of: {list(Action.__members__.keys())}")


InventoryLog.Schema = InventoryLogSchema
