from fastapi import FastAPI, Depends, HTTPException, status, Request
from src.db.configurations import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.api.users import router as users_router
from src.api.utils import router as utils_router

from src.api.exceptions import (
    UserNotFoundError,
    DuplicateEmailError,
    user_not_found_handler,
    duplicate_email_handler,
    ServerError,
    server_error_handler,
)
import time

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(DuplicateEmailError, duplicate_email_handler)
app.add_exception_handler(ServerError, server_error_handler)


app.include_router(users_router, prefix="/api")
app.include_router(utils_router, prefix="/api")
