from celery import Celery
from celery.schedules import schedule
from app.config import settings

celery_app = Celery(
    "pulse",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["workers.scheduler"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    # by  default celery marks a task done the moment a worker picks up, not when it finishes. this is the job acknowledgment behaviour.
    task_acks_late=True,
    # by default each worker grabs multiple tasks from the queue ahead of time.  If a worker prefetches 4 tasks and the first one hangs for 10s, the other 3 sit idle in that worker's local buffer while other workers might be starving. Setting this to 1 means a worker only takes a new task when it's actually free. Correct choice for variable-duration I/O tasks.
    worker_prefetch_multiplier=1,  # one task at a time per worker
)

celery_app.conf.beat_schedule = {
    "tick-scheduler": {
        "task": "workers.scheduler.tick",
        "schedule": schedule(run_every=10.0)
    },
}
