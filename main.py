from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.database import engine, Base
from app.utils.logging_config import logger
from app.api.v1.router import router as api_router
from app.core.dirs import IMAGES_DIR
from app.utils.rate_limit import limiter, add_rate_limit_exception_handler


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database models initialized.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()  # Initialize database models
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="My Blog 2.0 API",
    description="Backend API для личного блога",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter

add_rate_limit_exception_handler(app)

app.include_router(api_router, prefix="/api/v1")

app.mount("/public/images", StaticFiles(directory=IMAGES_DIR), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)