class MissingCommentUuid(ValueError):

    def __init__(self):
        self.message = "Missing Comment uuid"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class MissingNewCommentText(ValueError):

    def __init__(self):
        self.message = "Missing New Comment Text"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class MissingUserUuid(ValueError):

    def __init__(self):
        self.message = "Missing User uuid"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class MissingUserEmail(ValueError):

    def __init__(self):
        self.message = "Missing User Email"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class MissingUserPassword(ValueError):

    def __init__(self):
        self.message = "Missing User Password"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
