from jwt.exceptions import PyJWTError


class AccessTokenRequired(PyJWTError):

    def __init__(self):
        self.message = "Access Token Required"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
