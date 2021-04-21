from src.make_a_comment.adapters.request.basic import Request
from src.make_a_comment.adapters.response.basic import Response
from src.make_a_comment.use_case.service.user_interface import UserServiceInterface


class MakeACommentController:
    def __init__(self, user_service: UserServiceInterface):
        self.service = user_service

    def handle(self, request: Request) -> Response:

        request_payload = {"access_token": request.payload.get("access_token"),
                           "user_uuid": request.payload.get("user_uuid"),
                           "text": request.payload.get("text")}

        response = self.service.make_a_comment(**request_payload)

        return response
