from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from src.db.configurations import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserSchema
from src.schemas.auth import User
from src.services.auth import get_current_user
from src.services.users import UserService
from src.repository.users import UserRepository
from src.conf.limiter import limiter


router = APIRouter(prefix="/users", tags=["users"])


async def user_service(db: AsyncSession = Depends(get_db_session)):
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/me", response_model=User)
@limiter.limit("5/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    return user
