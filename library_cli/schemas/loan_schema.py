from marshmallow import fields, validates, ValidationError, Schema
from datetime import datetime


# Lazy imports for circular references


class LoanSchema(Schema):
    id = fields.Int(dump_only=True)
    copy_id = fields.Int(required=True)
    member_id = fields.Int(required=True)
    borrowed_at = fields.DateTime()
    returned_at = fields.DateTime(allow_none=True)

    # Custom validation
    @validates("returned_at")
    def validate_returned_at(self, value, **kwargs):
        if value and value > datetime.now():
            raise ValidationError("returned_at cannot be in the future.")

    @validates("borrowed_at")
    def validate_borrowed_at(self, value, **kwargs):
        if value and value > datetime.now():
            raise ValidationError("borrowed_at cannot be in the future.")
