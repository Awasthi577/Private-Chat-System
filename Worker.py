import asyncio
import logging
from typing import Callable, Awaitable

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

running_jobs: dict[str, asyncio.Task] = {}

async def rotate_keys():
    """Simulates a secure key rotation job."""
    while True:
        logger.info(" Rotating identity/prekeys...")
        await asyncio.sleep(30)

async def maintain_connection():
    """Maintains a secure relay or pub-sub connection."""
    while True:
        logger.info("🔗 Maintaining secure socket to relay...")
        await asyncio.sleep(15)

async def start_job(name: str, coro: Callable[[], Awaitable[None]]):
    """Starts a background job if not already running."""
    if name in running_jobs:
        logger.warning(f" Job '{name}' is already running.")
        return

    try:
        task = asyncio.create_task(_job_wrapper(name, coro))
        running_jobs[name] = task
        logger.info(f" Started job: {name}")
    except Exception as e:
        logger.error(f" Failed to start job '{name}': {e}")

async def _job_wrapper(name: str, coro: Callable[[], Awaitable[None]]):
    """Wraps job execution with error handling."""
    try:
        await coro()
    except asyncio.CancelledError:
        logger.info(f" Job '{name}' was cancelled.")
    except Exception as e:
        logger.exception(f" Unhandled exception in job '{name}': {e}")
    finally:
        running_jobs.pop(name, None)

async def shutdown_jobs():
    """Cancels and gracefully shuts down all running jobs."""
    logger.info(" Shutting down jobs...")
    for name, task in list(running_jobs.items()):
        logger.info(f" Cancelling job: {name}")
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            logger.info(f" Job '{name}' cancelled cleanly.")
