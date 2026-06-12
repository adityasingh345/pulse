from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings
from supabase import create_client
import uuid

# Supabase client — created once at module load
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# FastAPI's built-in Bearer token extractor
security = HTTPBearer()

DbSession = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> uuid.UUID:


    token = credentials.credentials


    try:
        response = supabase.auth.get_user(token)

        print("USER:", response.user)

        return uuid.UUID(response.user.id)

    except Exception as e:
        print("ERROR TYPE:", type(e))
        print("ERROR:", repr(e))
        raise


# Type alias for clean route signatures
CurrentUser = Annotated[uuid.UUID, Depends(get_current_user_id)]