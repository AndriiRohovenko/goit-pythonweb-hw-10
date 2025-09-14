from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from src.db.configurations import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserSchema
from src.schemas.auth import User
from src.services.auth import get_current_user
from src.services.users import UserService
from src.repository.users import UserRepository


router = APIRouter(prefix="/users", tags=["users"])


async def user_service(db: AsyncSession = Depends(get_db_session)):
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/me", response_model=User)
async def me(user: User = Depends(get_current_user)):
    return user
