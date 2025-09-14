from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth import create_access_token, Hash
from src.services.users import UserService
from src.repository.users import UserRepository
from src.db.configurations import get_db_session as get_db
from src.schemas.auth import UserCreate, Token, User

router = APIRouter(prefix="/auth", tags=["auth"])


async def user_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate, user_service: UserService = Depends(user_service)
):
    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    return await user_service.create_user(user_data)


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(user_service),
):
    user = await user_service.get_user_by_email(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"sub": user.email})
    refresh_token = await create_access_token(
        data={"sub": user.email}, expires_delta=7 * 24 * 3600
    )  # 7 days
    # save refresh_token in DB for user
    await user_service.update_refresh_token(user.id, refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
