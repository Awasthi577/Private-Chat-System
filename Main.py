from fastapi import FastAPI
import logging

from app.worker import start_job, shutdown_jobs, rotate_keys, maintain_connection

app = FastAPI()

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event() -> None:
    """Triggered when the application starts up."""
    try:
        await start_job("key_rotation", rotate_keys)
        await start_job("connection_maintainer", maintain_connection)
        logger.info(" Background jobs started successfully.")
    except Exception as e:
        logger.exception(f" Error while starting background jobs: {e}")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Triggered on graceful shutdown."""
    await shutdown_jobs()
    logger.info("🧹 Background jobs shut down cleanly.")

@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """Health check route."""
    return {"status": "Background jobs running"}
