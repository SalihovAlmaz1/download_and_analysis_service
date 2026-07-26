from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.project_config import settings
from src.core.lifespan import lifespan
from src.routes import get_apps_router

STATIC_DIR = Path(__file__).resolve().parent / "static"


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        lifespan=lifespan,
    )
    application.include_router(get_apps_router())

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)