class InvalidLoginCredentials(Exception):

    def __init__(self):
        self.message = "Invalid Login Credentials"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
