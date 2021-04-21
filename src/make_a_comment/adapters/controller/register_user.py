from src.make_a_comment.adapters.request.basic import Request
from src.make_a_comment.adapters.response.basic import Response
from src.make_a_comment.use_case.service.user_interface import UserServiceInterface


class RegisterUserController:

    def __init__(self, user_service: UserServiceInterface):
        self.service = user_service

    def handle(self, request: Request) -> Response:

        request_payload = {"name": request.payload.get("name"),
                           "email": request.payload.get("email"),
                           "password": request.payload.get("password"),
                           "admin": request.payload.get("admin")}

        response = self.service.register_user(**request_payload)

        return response
