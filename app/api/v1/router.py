from fastapi import APIRouter
from .posts import router as posts_router
from .comments import router as comments_router

router = APIRouter()

router.include_router(posts_router, prefix="/posts", tags=["posts"])
router.include_router(comments_router, prefix="/comments", tags=["comments"])