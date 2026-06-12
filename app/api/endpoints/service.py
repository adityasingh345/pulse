from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from uuid import UUID
from app.api.endpoints.models import Endpoint
from app.api.endpoints.schemas import EndpointCreate, EndpointUpdate

# flush() sends the SQL to the database within the current transaction but does not finalize it. The row exists temporarily — your session can see it, but no other connection can yet. The actual commit() happens in get_db() automatically after the route handler returns.

#If you only filter by id, any authenticated user can fetch, update, or delete any endpoint — they just need to guess a UUID. This is called an Insecure Direct Object Reference (IDOR)

async def create_endpoint(
    db: AsyncSession,
    user_id: UUID,
    data: EndpointCreate
) -> Endpoint:
    # Convert HttpUrl to string — SQLAlchemy expects a plain string
    endpoint = Endpoint(
        user_id=user_id,
        name=data.name,
        url=str(data.url),
        check_interval_seconds=data.check_interval_seconds,
    )
    db.add(endpoint)

    # Send SQL to DB, get server-side defaults populated
    await db.flush()

    # Pull the created_at and id back into the Python object
    await db.refresh(endpoint)

    return endpoint

async def get_user_endpoints(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 20,
    offset: int = 0,
) -> list[Endpoint]:
    stmt = (select(Endpoint).where(
        Endpoint.user_id == user_id
    ).limit(limit).offset(offset)
    )
    
    result = await db.execute(stmt)

    return result.scalars().all()

async def get_endpoint_by_id(
    db: AsyncSession,
    endpoint_id: UUID,
    user_id: UUID
) -> Endpoint | None:
    stmt = select(Endpoint).where(
       and_(Endpoint.user_id == user_id, Endpoint.id == endpoint_id)
    )
    result = await db.execute(stmt)
    
    return result.scalar_one_or_none()

async def update_endpoint(
    db: AsyncSession,
    endpoint_id: UUID,
    user_id: UUID,
    data: EndpointUpdate
) -> Endpoint | None:
    endpoint = await get_endpoint_by_id(
        db=db,
        endpoint_id = endpoint_id,
        user_id=user_id
    )

    if endpoint is None:
        return None
    
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(endpoint, field, value)

    await db.flush()
    await db.refresh(endpoint)

    return endpoint

async def delete_endpoint(
    db: AsyncSession,
    endpoint_id: UUID,
    user_id: UUID
) -> bool:
    endpoint = await get_endpoint_by_id(
        db=db,
        endpoint_id=endpoint_id,
        user_id=user_id
    )

    if endpoint is None:
        return False

    await db.delete(endpoint)
    await db.flush()

    return True

