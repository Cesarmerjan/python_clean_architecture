from .user import User


class System:
    def __init__(self):
        self.users = set()

    def register_a_user(self, user: User) -> None:
        if not user in self.users:
            self.users.add(user)

    def __repr__(self):
        return f"<System>"

    def __str__(self):
        return f"system have {len(self.users)} users"
