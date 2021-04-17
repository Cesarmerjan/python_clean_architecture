from src.make_a_comment.adapters.input.interface import InputInterface
from src.make_a_comment.serializer.comment import comment_serializer


class CommentUuidOnlyInput(InputInterface):

    def __init__(self, data: dict):
        self._comment_uuid = None
        self.comment_uuid: str = data.get("comment_uuid")

    def to_dict(self):
        return {
            "comment_uuid": self.comment_uuid,
        }

    @property
    def comment_uuid(self) -> str:
        return self._comment_uuid

    @comment_uuid.setter
    def comment_uuid(self, comment_uuid: str) -> None:
        comment_serializer.declared_fields.get(
            "uuid").deserialize(comment_uuid)

        self._comment_uuid = comment_uuid
