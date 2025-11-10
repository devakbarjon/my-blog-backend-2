from typing import Optional
import uuid
from fastapi import APIRouter, Depends, File, Form, Header, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.posts import get_all_posts, get_post_by_id, create_post, increment_post_views
from app.models.schemas.errors import ErrorResponse
from app.models.schemas.posts import PostListResponse, PostIn, PostOut
from app.core.config import settings
from app.core.dirs import IMAGES_DIR
import shutil

router = APIRouter()


@router.get("/", response_model=PostListResponse)
async def get_posts(session: AsyncSession = Depends(get_db)):
    posts = await get_all_posts(session=session)
    
    return PostListResponse(posts=posts)



@router.get("/{post_id}", response_model=PostOut | ErrorResponse)
async def get_post(
     post_id: int, 
     viewer_id: str | None = Header(None), 
     session: AsyncSession = Depends(get_db)
    ):
    post = await get_post_by_id(session=session, post_id=post_id)

    if not post:
        return ErrorResponse(
            code="post_not_found",
            message="The requested post does not exist."
        )
    
    if viewer_id:
        await increment_post_views(session=session, post_id=post_id, viewer_id=viewer_id)
    
    return PostOut.model_validate(post)


@router.post("/", response_model=PostOut | ErrorResponse)
async def admin_create_post(
     post_form: str = Form(...), 
     session: AsyncSession = Depends(get_db),
     image: Optional[UploadFile] = File(None),
    ):
        try:
            post = PostIn.model_validate_json(post_form)
        except Exception:
            return ErrorResponse(code="invalid_data", message="Invalid post data")
        
        if post.secret_word != settings.secret_word:
            return ErrorResponse(
                code="unauthorized",
                message="Invalid secret word provided."
            )
        
        post_data = post.model_dump()
        post_data.pop("secret_word", None)  # Remove secret_word before creating the post

        image_filename = None
        if post_data["image"] is True and image:
            unique_name = f"{uuid.uuid4().hex}_{image.filename}"
            image_path = IMAGES_DIR / unique_name
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_filename = unique_name

        post_data["image"] = image_filename

        new_post = await create_post(session=session, **post_data)

        if not new_post:
            return ErrorResponse(
                code="creation_failed",
                message="Failed to create the post."
            )

        return PostOut.model_validate(new_post)