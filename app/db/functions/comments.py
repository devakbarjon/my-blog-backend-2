from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment


async def save_comment(session: AsyncSession, post_id: int, author: str, content: str) -> Comment:
    new_comment = Comment(
        post_id=post_id,
        author=author,
        content=content
    )
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment