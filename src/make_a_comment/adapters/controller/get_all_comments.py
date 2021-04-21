from src.make_a_comment.adapters.request.basic import Request
from src.make_a_comment.adapters.response.basic import Response
from src.make_a_comment.use_case.service.comment_interface import CommentServiceInterface


class GetAllCommentsController:
    def __init__(self, comment_service: CommentServiceInterface):
        self.service = comment_service

    def handle(self, request: Request) -> Response:

        request_payload = {}

        response = self.service.get_all_comments(**request_payload)

        return response
