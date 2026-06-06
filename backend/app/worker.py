import os
from celery import Celery
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Initialize Celery app
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    # Max time a task can run before being killed
    task_time_limit=600,
    task_soft_time_limit=540,
)

@celery_app.task(bind=True, name="process_repository_task")
def process_repository_task(self, repo_id: str, url: str):
    """
    Celery task to process a repository in the background.
    """
    from app.services.worker import process_repository
    # We must run the async function using asyncio
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(process_repository(repo_id, url))
        return {"status": "success", "repo_id": repo_id}
    except Exception as e:
        return {"status": "error", "message": str(e), "repo_id": repo_id}
