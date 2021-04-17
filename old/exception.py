class RequestDataException(ValueError):

    def __init__(self, parameter: str, error: str):
        self.parameter = parameter
        self.error = error
        self.message = f"'{self.parameter}': {self.error}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
