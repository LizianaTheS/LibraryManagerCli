from marshmallow import fields, validates, ValidationError, Schema

from library_cli.static import Status

from datetime import datetime


class ReservationSchema(Schema):
    id = fields.Int(dump_only=True)

    member_id = fields.Int(required=True)
    copy_id = fields.Int(required=True)

    reserved_at = fields.DateTime(required=True)
    expires_at = fields.DateTime(required=True)

    status = fields.Str(required=True)

    # Validation
    @validates("expires_at")
    def validate_expires_at(self, value, **kwargs):
        if value < datetime.now():
            raise ValidationError("expires_at cannot be in the past.")

    @validates("status")
    def validate_status(self, value, **kwargs):
        if value not in Status.__members__:
            raise ValidationError(f"Invalid status: {value}. Must be one of: {list(Status.__members__.keys())}")
