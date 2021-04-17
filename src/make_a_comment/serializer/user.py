from marshmallow import Schema, fields
from marshmallow.validate import Length
from marshmallow import pre_dump, pre_dump

from .comment import CommentSerializer


class UserSerializer(Schema):
    # dump_only
    uuid = fields.Str(required=True,
                      allow_none=False,
                      validate=Length(equal=36),
                      dump_only=True)

    comments = fields.Nested(CommentSerializer, many=True, dump_only=True)

    # load_only
    password = fields.Str(validate=Length(min=8, max=25), required=True,
                          load_only=True)

    # others
    name = fields.Str(validate=Length(min=3, max=30),
                      required=True, allow_none=False)

    email = fields.Email(required=True, validate=Length(min=10, max=30))

    admin = fields.Bool(required=False, allow_none=True, default=False)


user_serializer = UserSerializer()
