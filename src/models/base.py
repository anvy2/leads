from datetime import datetime

import sqlalchemy
from sqlmodel import Field, SQLModel
from ulid import ULID

SQLModel.__table_args__ = {"extend_existing": True}


def generate_id() -> str:
    return str(ULID())


class BaseModel(SQLModel):
    id: str = Field(default_factory=generate_id, primary_key=True)
    created_at: datetime = Field(default_factory=sqlalchemy.func.now)
    updated_at: datetime = Field(
        default_factory=sqlalchemy.func.now, sa_column_kwargs={"onupdate": sqlalchemy.func.now}
    )
