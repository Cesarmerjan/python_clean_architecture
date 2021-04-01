from sqlalchemy import Table, Column, ForeignKey, String, DateTime
from src.make_a_comment.adapters.orm import metadata


comments_table = Table(
    "comments", metadata,
    Column("uuid", String(36), primary_key=True),
    Column("text", String(255), nullable=False),
    Column("datetime", DateTime, nullable=False),
    Column("user_uuid", String(36), ForeignKey("users.uuid"), nullable=False)
)
