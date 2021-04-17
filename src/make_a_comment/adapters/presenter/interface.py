import abc


class PresenterInterface:

    request: "RequestObject"
    response: "ResponseObject"

    @abc.abstractmethod
    def parse_request(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def build_response(self) -> "ResponseObject":
        raise NotImplementedError
