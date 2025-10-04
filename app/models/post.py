from sqlalchemy import (
    Column, ForeignKey, Text, BigInteger, Boolean, Integer,
    DateTime, func
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.db.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(ARRAY(Text), default=list)
    image = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __init__(self, title: str, body: str, tags: list[str] = None, image: str = None):
        self.title = title
        self.body = body
        self.tags = tags if tags is not None else []
        self.image = image

    def __repr__(self):
        return f"<Post(id={self.id})>"
