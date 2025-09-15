from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import extract, and_, or_, select
from datetime import date, timedelta
from src.db.models import User


class AuthRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
