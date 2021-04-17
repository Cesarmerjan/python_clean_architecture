from src.make_a_comment.adapters.input.interface import InputInterface
from src.make_a_comment.serializer.user import user_serializer


class RegisterUserInput(InputInterface):

    def __init__(self, data):
        self._name = None
        self.name: str = data.get("name")
        self._email = None
        self.email: str = data.get("email")
        self._password = None
        self.password: str = data.get("password")
        self._admin = None
        self.admin: bool = data.get("admin")

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "admin": self.admin
        }

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        user_serializer.declared_fields.get(
            "name").deserialize(name)
        self._name = name

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

    @property
    def admin(self) -> str:
        return self._admin

    @admin.setter
    def admin(self, admin: bool) -> None:
        user_serializer.declared_fields.get(
            "admin").deserialize(admin)
        self._admin = admin
