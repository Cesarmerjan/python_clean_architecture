from src.make_a_comment.adapters.input.interface import InputInterface
from src.make_a_comment.serializer.user import user_serializer


class LoginUserInput(InputInterface):

    def __init__(self, data):
        self._email = None
        self.email: str = data.get("email")
        self._password = None
        self.password: str = data.get("password")

    # torcar to_dict, por uma propriedade parsed_input
    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password
        }

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        user_serializer.declared_fields.get(
            "email").deserialize(email)
        self._email = email

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        user_serializer.declared_fields.get(
            "password").deserialize(password)
        self._password = password
