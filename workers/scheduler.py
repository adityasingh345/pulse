from celery import shared_task
from sqlalchemy import text
import asyncio
from app.database import AsyncSessionLocal
from workers.celery_app import celery_app
from workers.db import SessionLocal

import redis 
from app.config import settings
import json 

redis_client = redis.from_url(settings.REDIS_URL)

@celery_app.task(name="workers.scheduler.tick")
def tick():
    with SessionLocal() as db:
        stmt = text("""
            UPDATE endpoints
            SET next_check_at = NOW() + (check_interval_seconds * interval '1 second')
            WHERE id IN (
                SELECT id
                FROM endpoints
                WHERE is_active = true
                  AND next_check_at <= NOW()
                ORDER BY next_check_at
                -- FOR UPDATE locks selected rows until the transaction commits
                -- SKIP LOCKED skips rows already locked by another transaction
                FOR UPDATE SKIP LOCKED
            )
            RETURNING id, url, check_interval_seconds
        """)

        result = db.execute(stmt)
        claimed = result.fetchall()
        db.commit()


        for row in claimed:
            check_endpoint.delay(
                endpoint_id=str(row.id),
                url=row.url,
                timeout=10,
            )

