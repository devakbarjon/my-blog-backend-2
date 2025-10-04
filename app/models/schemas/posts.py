from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict, field_serializer

from app.models.schemas.comments import CommentOut

from .base import BaseResponse


class PostIn(BaseModel):
    title: str
    body: str
    tags: list[str] = Field(default_factory=list)
    image: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    id: int
    title: str
    body: str
    tags: list[str] = Field(default_factory=list)
    image: str | None = None
    comments: List[CommentOut] = []
    created_at: str

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

    model_config = ConfigDict(from_attributes=True)


class PostListResponse(BaseResponse):
    posts: list[PostOut] = []