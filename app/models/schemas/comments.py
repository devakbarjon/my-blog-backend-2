from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_serializer
from .base import BaseResponse


class CommentIn(BaseModel):
    author: str
    content: str
    post_id: int

class CommentOut(BaseModel):
    id: int
    author: str
    content: str
    post_id: int
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

    model_config = ConfigDict(from_attributes=True)


class CommentListResponse(BaseResponse):
    comments: list[CommentOut] = []