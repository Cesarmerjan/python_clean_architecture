from src.make_a_comment.adapters.input.interface import InputInterface
from src.make_a_comment.serializer.user import user_serializer


class UserUuidOnlyInput(InputInterface):

    def __init__(self, data: dict):
        self._user_uuid = None
        self.user_uuid: str = data.get("user_uuid")

    def to_dict(self):
        return {
            "user_uuid": self.user_uuid,
        }

    @property
    def user_uuid(self) -> str:
        return self._user_uuid

    @user_uuid.setter
    def user_uuid(self, user_uuid: str) -> None:
        user_serializer.declared_fields.get(
            "uuid").deserialize(user_uuid)

        self._user_uuid = user_uuid
