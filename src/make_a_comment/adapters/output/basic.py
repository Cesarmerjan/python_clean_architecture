class BasicOutput:
    def __init__(self, http_status_code: int, message: str, data: dict = {}):
        self.http_status_code = http_status_code
        self.message = self._format_message(message)
        self.data = data

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, str(msg))
        return msg
