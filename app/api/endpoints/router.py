from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from app.api.endpoints.schemas import (
    EndpointCreate,
    EndpointUpdate,
    EndpointResponse
)
from app.api.endpoints import service
from app.dependencies import DbSession, CurrentUser

router = APIRouter(prefix="/endpoints", tags=["endpoints"])


@router.post("/", response_model=EndpointResponse, status_code=201)
async def create_endpoint(
    data: EndpointCreate,
    db: DbSession,
    current_user_id: CurrentUser
):
    # TODO: call service.create_endpoint, return result
    return await service.create_endpoint(
        db=db,
        user_id= current_user_id,
        data=data
    )


@router.get("/", response_model=list[EndpointResponse])
async def list_endpoints(
    db: DbSession,
    current_user_id: CurrentUser,
    limit: int = 20,
    offset: int = 0
):
    return await service.get_user_endpoints(
        db=db,
        user_id=current_user_id,
        limit= limit,
        offset=offset
    )


@router.get("/{endpoint_id}", response_model=EndpointResponse)
async def get_endpoint(
    endpoint_id: UUID,
    db: DbSession,
    current_user_id:  CurrentUser
):
    endpoint = await service.get_endpoint_by_id(
        endpoint_id=endpoint_id,
        db=db,
        user_id=current_user_id
    )
    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found"
        )
    return endpoint


@router.patch("/{endpoint_id}", response_model=EndpointResponse)
async def update_endpoint(
    endpoint_id: UUID,
    data: EndpointUpdate,
    db: DbSession,
    current_user_id:  CurrentUser
):
    endpoint = await service.update_endpoint(
        db=db,
        endpoint_id=endpoint_id,
        user_id=current_user_id,
        data=data
    )

    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found"
        )

    return endpoint
    


@router.delete("/{endpoint_id}", status_code=204)
async def delete_endpoint(
    endpoint_id: UUID,
    db: DbSession,
    current_user_id: CurrentUser
):
    deleted = await service.delete_endpoint(
        db=db, 
        endpoint_id=endpoint_id,
        user_id=current_user_id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found"
        )

    return None