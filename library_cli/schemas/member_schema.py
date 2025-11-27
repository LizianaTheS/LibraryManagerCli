from marshmallow import fields, ValidationError, validates, Schema, validate

from library_cli.static import Status


class MemberSchema(Schema):
    id = fields.Int(dump_only=True)
    fullname = fields.Str(required=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    phone = fields.Str(required=False, validate=validate.Length(max=15), allow_none=True)
    status = fields.Str(required=True)

    # Nested relationships, manually controlled

    @validates("status")
    def validate_status(self, value, **kwargs):
        if value.upper() not in Status.__members__:
            raise ValidationError(f"Invalid status: {value}. Must be one of: {list(Status.__members__.keys())}")

# from marshmallow import fields, validates, ValidationError, validate
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from library_cli.static import Status
# from library_cli.models import Member
#
#
# class MemberSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         (model) = Member
#         load_instance = True
#         include_relationships = True
#
#     id = fields.Int(dump_only=True)
#     fullname = fields.Str(required=True, validate=validate.Length(max=100))
#     username = fields.Str(required=True, validate=validate.Length(max=100))
#     password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
#     email = fields.Email(required=True, validate=validate.Length(max=150))
#     phone = fields.Str(required=False, validate=validate.Length(max=15))
#     status = fields.Str(required=False)
#     # Nested relationships
#     logs = fields.List(fields.Nested("InventoryLogSchema", exclude=("member",)), required=False)
#     loans = fields.List(fields.Nested("LoanSchema", exclude=("member",)), required=False)
#     reservations = fields.List(fields.Nested("ReservationSchema", exclude=("member",), required=False))
#
#     @validates("status")
#     def validate_status(self, value):
#         if value not in Status.__members__:
#             raise ValidationError(f"{value} is not a valid Status.")
#
#
# Member.Schema = MemberSchema
