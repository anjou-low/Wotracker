from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from config import settings

app = FastAPI()

if settings.BACKEND_CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin for origin in settings.BACKEND_CORS_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app.include_router(api_router)