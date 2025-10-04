from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post

async def get_all_posts(session: AsyncSession) -> list[Post]:
    result = await session.execute(
        select(Post).order_by(Post.id)
    )
    posts = result.scalars().all()
    return posts

async def get_post_by_id(session: AsyncSession, post_id: int) -> Post | None:
    result = await session.execute(
        select(Post).where(Post.id == post_id)
    )
    return result.scalars().first()