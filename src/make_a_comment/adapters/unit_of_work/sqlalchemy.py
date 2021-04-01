from sqlalchemy.orm import Session
from .interface import UoWInterface
from src.make_a_comment.adapters.repository.interface import RepositoryInterface


class SqlAlchemyUoW(UoWInterface):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self, repository):
        self.session = self.session_factory()  # type: Session
        self.repository = repository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
