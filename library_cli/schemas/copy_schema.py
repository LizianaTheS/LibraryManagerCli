from library_cli.static import Condition, Action
from marshmallow import Schema, fields, validates, ValidationError


class CopySchema(Schema):
    id = fields.Int(dump_only=True)
    barcode = fields.Str(required=True, validate=lambda s: len(s) <= 50)
    book_id = fields.Int(required=True)
    # Enums as strings
    condition = fields.Str(required=True)
    action = fields.Str(required=True)

    @validates("condition")
    def validate_condition(self, value, **kwargs):
        if value not in Condition.__members__:
            raise ValidationError(f"Invalid condition: {value}. Must be one of: {list(Condition.__members__.keys())}")

    @validates("action")
    def validate_action(self, value, **kwargs):
        if value not in Action.__members__:
            raise ValidationError(f"Invalid action: {value}. Must be one of: {list(Action.__members__.keys())}")

# class CopySchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Copy
#         load_instance = True
#         include_relationships = True
#
#     id = fields.Int(dump_only=True)
#     barcode = fields.Str(required=True, validate=lambda s: len(s) <= 50)
#
#     # Enums
#     condition = fields.Enum(Condition, required=True)
#     action = fields.Enum(Action, required=True)
#
#     # Relationships
#
#     # book = fields.Nested("BookSchema", exclude=("copies",), required=True)
#     loans = fields.List(fields.Nested("LoanSchema", exclude=("copy",)), required=False)
#
#     # Validation
#     @validates("condition")
#     def validate_condition(self, value, **kwargs):
#         if not isinstance(value, Condition):
#             raise ValidationError(f"{value} is not a valid Condition.")
#
#     @validates("action")
#     def validate_action(self, value, **kwargs):
#         if not isinstance(value, Action):
#             raise ValidationError(f"{value} is not a valid Action.")
#
#
# Copy.Schema = CopySchema
