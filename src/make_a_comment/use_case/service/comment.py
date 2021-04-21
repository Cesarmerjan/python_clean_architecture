from typing import List
from copy import deepcopy
from functools import wraps

from src.make_a_comment.domain.comment import Comment

from .comment_interface import CommentServiceInterface
from src.make_a_comment.adapters.presenter.interface import PresenterInterface
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.adapters.response.type import ResponseType
from src.make_a_comment.adapters.response.basic import Response

from .login_required import login_required

from src.make_a_comment.adapters.response.custom_typing import PositiveResponse


class CommentService(CommentServiceInterface):

    def __init__(self, comment_uow: UoWInterface, presenter: PresenterInterface):
        self.uow = comment_uow
        self.presenter = presenter

    def build_response(positive_response: PositiveResponse):
        def inner_function(function):
            @wraps(function)
            def wrapper(self, *args, **kwargs):
                response = self.presenter.build_response(
                    function,
                    positive_response
                )(self, *args, **kwargs)
                return response
            return wrapper
        return inner_function

    @build_response(ResponseType.SUCCESS)
    @login_required
    def delete_comment_by_uuid(self, access_token, *args, **kwargs) -> Response:
        return self._delete_comment_by_uuid(*args, **kwargs)

    def _delete_comment_by_uuid(self, comment_uuid: "Comment.uuid") -> None:
        with self.uow:
            comment = self.uow.repository.get_by(uuid=comment_uuid)
            self.uow.repository.delete(comment)
            self.uow.commit()

    @build_response(ResponseType.SUCCESS)
    @login_required
    def get_comment_by_uuid(self, access_token, *args, **kwargs) -> Response:
        return self._get_comment_by_uuid(*args, **kwargs)

    def _get_comment_by_uuid(self, comment_uuid: "Comment.uuid") -> Comment:
        with self.uow:
            comment = self.uow.repository.get_by(uuid=comment_uuid)
            comment_copy = deepcopy(comment)
        return comment_copy

    @build_response(ResponseType.SUCCESS)
    @login_required
    def update_comment_by_uuid(self, access_token, *args, **kwargs) -> Response:
        return self._update_comment_by_uuid(*args, **kwargs)

    def _update_comment_by_uuid(self, comment_uuid: "Comment.uuid", new_text: str) -> Comment:
        with self.uow:
            comment = self.uow.repository.get_by(uuid=comment_uuid)
            comment.text = new_text
            comment_copy = deepcopy(comment)
            self.uow.repository.add(comment)
            self.uow.commit()
            return comment_copy

    @build_response(ResponseType.SUCCESS)
    def get_all_comments(self, *args, **kwargs) -> Response:
        return self._get_all_comments(*args, **kwargs)

    def _get_all_comments(self) -> List[Comment]:
        with self.uow:
            comments = self.uow.repository.get_all()
            comment_copy = deepcopy(comments)
        return comment_copy
