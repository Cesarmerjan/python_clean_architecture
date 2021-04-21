import abc
from typing import List
from src.make_a_comment.domain.comment import Comment

from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface
from src.make_a_comment.adapters.presenter.interface import PresenterInterface

from src.make_a_comment.adapters.response.basic import Response

from src.make_a_comment.adapters.response.custom_typing import PositiveResponse


class CommentServiceInterface(metaclass=abc.ABCMeta):

    comment_uow: UoWInterface
    presenter: PresenterInterface

    @abc.abstractmethod
    def build_response(positive_response: PositiveResponse):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_comment_by_uuid(self, access_token, *args, **kwargs) -> Response:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_comment_by_uuid(self, comment_uuid: "Comment.uuid") -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_comment_by_uuid(self, access_token, *args, **kwargs) -> Response:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_comment_by_uuid(self, comment_uuid: "Comment.uuid") -> Comment:
        raise NotImplementedError

    @abc.abstractmethod
    def update_comment_by_uuid(self, access_token, *args, **kwargs) -> Response:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_comment_by_uuid(self, comment_uuid: "Comment.uuid", new_text: str) -> Comment:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_comments(self, *args, **kwargs) -> Response:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all_comments(self) -> List[Comment]:
        raise NotImplementedError
