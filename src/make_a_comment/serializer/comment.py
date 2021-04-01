from marshmallow import Schema, fields
from marshmallow.validate import Length


class CommentSerializer(Schema):

    # dump_only
    uuid = fields.Str(required=True,
                      allow_none=False,
                      validate=Length(equal=36),
                      dump_only=True)

    datetime = fields.DateTime(required=True,
                               allow_none=False,
                               dump_only=True)

    # others
    text = fields.String(required=True, allow_none=False,
                         validate=Length(max=255))


comment_serializer = CommentSerializer()
