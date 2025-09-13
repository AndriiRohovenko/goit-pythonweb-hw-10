from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from src.db.configurations import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserSchema
from src.services.users import UserService
from src.repository.users import UserRepository

from src.schemas.error import ErrorResponse


router = APIRouter(prefix="/users", tags=["users"])


async def user_service(db: AsyncSession = Depends(get_db_session)):
    repo = UserRepository(db)
    return UserService(repo)


@router.get(
    "/",
    response_model=list[UserSchema],
)
async def get_users(
    skip: int = 0, limit: int = 25, service: UserService = Depends(user_service)
):
    return await service.get_users(skip=skip, limit=limit)


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchema, service: UserService = Depends(user_service)):
    return await service.create_user(user)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, service: UserService = Depends(user_service)):
    return await service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int, user: UserSchema, service: UserService = Depends(user_service)
):
    return await service.update_user(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(user_service)):
    await service.delete_user(user_id)


@router.get("/search/", response_model=list[UserSchema])
async def search_users(
    name: str | None = Query(None, description="Filter by name"),
    surname: str | None = Query(None, description="Filter by surname"),
    email: str | None = Query(None, description="Filter by email"),
    service: UserService = Depends(user_service),
):
    return await service.search_users(name, surname, email)


@router.get("/upcoming-birthdays/", response_model=list[UserSchema])
async def get_upcoming_birthdays(service: UserService = Depends(user_service)):
    return await service.upcoming_birthdays()
