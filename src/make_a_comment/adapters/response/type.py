from typing import ClassVar


class ResponseType:
    SUCCESS: ClassVar[str] = "SUCCESS"
    CREATED: ClassVar[str] = "CREATED"
    BAD_REQUEST: ClassVar[str] = "BAD_REQUEST"
    UNAUTHORIZED: ClassVar[str] = "UNAUTHORIZED"
    NOT_FOUND: ClassVar[str] = "NOT_FOUND"
    INTERNAL_SERVER_ERROR: ClassVar[str] = "INTERNAL_SERVER_ERROR"
