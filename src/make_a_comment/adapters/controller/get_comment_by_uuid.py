from src.make_a_comment.adapters.request.basic import Request
from src.make_a_comment.adapters.response.basic import Response
from src.make_a_comment.use_case.service.comment_interface import CommentServiceInterface


class GetCommentController:
    def __init__(self, comment_service: CommentServiceInterface):
        self.service = comment_service

    def handle(self, request: Request) -> Response:

        request_payload = {"access_token": request.payload.get("access_token"),
                           "comment_uuid": request.payload.get("comment_uuid")}

        response = self.service.get_comment_by_uuid(**request_payload)

        return response
