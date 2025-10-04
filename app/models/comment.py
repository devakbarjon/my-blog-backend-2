from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    post = relationship("Post", back_populates="comments")

    def __init__(self, author: str, content: str, post_id: int):
        self.author = author
        self.content = content
        self.post_id = post_id

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id})>"
