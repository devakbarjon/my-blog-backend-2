from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.models.post import Post

async def get_all_posts(session: AsyncSession) -> list[Post]:
    result = await session.execute(
        select(Post)
        .order_by(Post.id)
        .options(selectinload(Post.comments))
    )
    posts = result.scalars().all()
    return posts

async def get_post_by_id(session: AsyncSession, post_id: int) -> Post | None:
    result = await session.execute(
        select(Post).where(Post.id == post_id).options(selectinload(Post.comments))
    )
    return result.scalars().first()


async def create_post(session: AsyncSession, **kwargs) -> Post:
    new_post = Post(**kwargs)
    session.add(new_post)

    try:
        await session.commit()
        await session.refresh(new_post)

        result = await session.execute(
            select(Post)
            .options(selectinload(Post.comments))
            .where(Post.id == new_post.id)
        )
        
        post_with_comments = result.scalars().first()

        return post_with_comments

    except SQLAlchemyError:
        await session.rollback()
        raise

async def increment_post_views(session: AsyncSession, post_id: int, viewer_id) -> None:
    post = await get_post_by_id(session, post_id)

    if not post:
        return
    
    if viewer_id not in post.viewers:
        post.views += 1
        post.viewers = post.viewers + [viewer_id]
        try:
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
    
    return