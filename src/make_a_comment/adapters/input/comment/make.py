from src.make_a_comment.adapters.input.interface import InputInterface
from src.make_a_comment.adapters.serializer.comment import comment_serializer
from src.make_a_comment.utils.jwt_handler import validate_access_token

from src.make_a_comment.exceptions.access_token_required import AccessTokenRequired


class MakeCommentInput(InputInterface):

    def __init__(self, data: dict):
        self._text = None
        self.text: str = data.get("text")
        self._access_token = None
        self.access_token: str = data.get("access_token")

    def to_dict(self):
        return {
            "text": self.text
        }

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        comment_serializer.declared_fields.get(
            "text").deserialize(text)

        self._text = text

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, access_token: str) -> None:
        if not access_token:
            raise AccessTokenRequired
        validate_access_token(access_token)
        self._access_token = access_token
