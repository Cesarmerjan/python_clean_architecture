from sqlalchemy import Table, Column, String, Boolean
from src.make_a_comment.adapters.orm import metadata


users_table = Table(
    "users", metadata,
    Column("uuid", String(36), primary_key=True),
    Column("name", String(30), nullable=False),
    Column("email", String(30), nullable=False, unique=True),
    Column("password_hash", String(128), nullable=False),
    Column("admin", Boolean, nullable=False, default=False)
)
