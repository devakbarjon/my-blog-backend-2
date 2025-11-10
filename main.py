from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.database import engine, Base
from app.utils.logging_config import logger
from app.api.v1.router import router as api_v1_router
from app.core.dirs import IMAGES_DIR


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database models initialized.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()  # Initialize database models
    yield
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_router, prefix="/api/v1")

app.mount("/public/images", StaticFiles(directory=IMAGES_DIR), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)