from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.comments import save_comment
from app.models.schemas.comments import CommentIn, CommentOut
from app.models.schemas.errors import ErrorResponse

router = APIRouter()


@router.post("/", response_model=CommentOut)
async def create_comment(comment: CommentIn, session: AsyncSession = Depends(get_db)):

    new_comment = await save_comment(
        session=session,
        post_id=comment.post_id,
        author=comment.author,
        content=comment.content
    )

    if not new_comment:
        return ErrorResponse(
            code="comment_creation_failed",
            message="Failed to create the comment."
        )

    return CommentOut.model_validate(new_comment)