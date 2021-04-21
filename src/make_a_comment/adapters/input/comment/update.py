from src.make_a_comment.adapters.input.interface import InputInterface
from src.make_a_comment.adapters.serializer.comment import comment_serializer
from src.make_a_comment.utils.jwt_handler import validate_access_token

from src.make_a_comment.exceptions.access_token_required import AccessTokenRequired


class UpdateCommentInput(InputInterface):

    def __init__(self, data: dict):
        self._comment_uuid = None
        self.comment_uuid: str = data.get("comment_uuid")
        self._new_text = None
        self.new_text: str = data.get("new_text")
        self._access_token = None
        self.access_token: str = data.get("access_token")

    def to_dict(self):
        return {
            "comment_uuid": self.comment_uuid,
            "new_text": self.new_text
        }

    @property
    def comment_uuid(self) -> str:
        return self._comment_uuid

    @comment_uuid.setter
    def comment_uuid(self, comment_uuid: str) -> None:
        comment_serializer.declared_fields.get(
            "uuid").deserialize(comment_uuid)

        self._comment_uuid = comment_uuid

    @property
    def new_text(self) -> str:
        return self._new_text

    @new_text.setter
    def new_text(self, new_text: str) -> None:
        comment_serializer.declared_fields.get(
            "text").deserialize(new_text)

        self._new_text = new_text

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, access_token: str) -> None:
        if not access_token:
            raise AccessTokenRequired
        validate_access_token(access_token)
        self._access_token = access_token
