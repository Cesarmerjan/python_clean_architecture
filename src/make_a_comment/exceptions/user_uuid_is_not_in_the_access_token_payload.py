from jwt.exceptions import PyJWTError


class UserUuidIsNotInAccessTokenPayload(PyJWTError):

    def __init__(self):
        self.message = "User Uuid Is Not In Access Token Payload"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
