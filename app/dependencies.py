from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

# Type alias — use this in every route that needs a DB session
DbSession = Annotated[AsyncSession, Depends(get_db)]