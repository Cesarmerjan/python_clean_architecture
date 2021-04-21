from src.make_a_comment.adapters.request.basic import Request
from src.make_a_comment.adapters.response.basic import Response
from src.make_a_comment.use_case.service.user_interface import UserServiceInterface


class GetUserController:
    def __init__(self, user_service: UserServiceInterface):
        self.service = user_service

    def handle(self, request: Request) -> Response:

        request_payload = {"user_uuid": request.payload.get("user_uuid")}

        response = self.service.get_user_by_uuid(**request_payload)

        return response
