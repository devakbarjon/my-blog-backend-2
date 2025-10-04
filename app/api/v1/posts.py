from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.posts import get_all_posts, get_post_by_id
from app.models.schemas.errors import ErrorResponse
from app.models.schemas.posts import PostListResponse, PostIn, PostOut

router = APIRouter()


@router.get("/", response_model=PostListResponse)
async def get_posts(session: AsyncSession = Depends(get_db)):
    posts = await get_all_posts(session=session)
    
    return PostListResponse(posts=posts)



@router.get("/{post_id}", response_model=PostOut | ErrorResponse)
async def get_post(post_id: int, session: AsyncSession = Depends(get_db)):
    post = await get_post_by_id(session=session, post_id=post_id)

    if not post:
        return ErrorResponse(
            code="post_not_found",
            message="The requested post does not exist."
        )
    
    return PostOut.model_validate(post)


@router.post("/", response_model=PostOut | ErrorResponse)
async def create_post(post: PostIn, session: AsyncSession = Depends(get_db)):
    ...