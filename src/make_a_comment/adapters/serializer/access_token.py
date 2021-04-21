from marshmallow import Schema, fields
from src.make_a_comment.utils.jwt_handler import validate_access_token


class AccessTokenSchema(Schema):

    access_token = fields.Str(required=True,
                              allow_none=False,
                              validate=validate_access_token)


access_token_schema = AccessTokenSchema()
