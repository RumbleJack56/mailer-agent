from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server import __version__
from server.config import settings

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": __version__}
