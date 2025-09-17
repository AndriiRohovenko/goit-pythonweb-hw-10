from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth import create_access_token, Hash, get_current_user
from src.services.users import UserService
from src.repository.users import UserRepository
from src.db.configurations import get_db_session as get_db
from src.schemas.auth import UserCreate, Token, User, RefreshTokenRequest
from src.conf.config import config

from src.services.email import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])


async def user_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    user_service: UserService = Depends(user_service),
):
    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    token = await create_access_token(
        data={"sub": user_data.email},
        expires_delta=24 * config.JWT_EXPIRATION_SECONDS,
    )

    background_tasks.add_task(
        send_verification_email, user_data.email, token, user_info=user_data
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

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
        )

    access_token = await create_access_token(data={"sub": user.email})
    refresh_token = await create_access_token(
        data={"sub": user.email}, expires_delta=7 * 24 * 3600
    )  # 7 days
    # save refresh_token in DB for user
    await user_service.update_refresh_token(user, refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    body: RefreshTokenRequest,
    user_service: UserService = Depends(user_service),
):
    print(body.refresh_token)
    if body.refresh_token is None:
        raise HTTPException(status_code=400, detail="Refresh token is required")
    user = await user_service.get_user_by_refresh_token(body.refresh_token)
    print(user)

    if not user or user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db_refresh_token = await user_service.get_refresh_token(user)
    print(db_refresh_token)
    if db_refresh_token != body.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": db_refresh_token,
        "token_type": "bearer",
    }


@router.get("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(token: str, user_service: UserService = Depends(user_service)):
    print(token)
    user = await user_service.get_user_by_email_verification_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
        )

    await user_service.verify_email(user)
    return {"detail": "Email verified successfully"}
