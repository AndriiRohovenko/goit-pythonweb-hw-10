from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import extract, and_, or_, select
from datetime import date, timedelta
from src.db.models import User


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, limit: int, skip: int):
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, existing_user: User, data: dict):
        for field, value in data.items():
            setattr(existing_user, field, value)
        await self.db.commit()
        await self.db.refresh(existing_user)
        return existing_user

    async def delete(self, user: User):
        await self.db.delete(user)
        await self.db.commit()

    async def search(self, name: str | None, surname: str | None, email: str | None):
        query = select(User)

        if name:
            query = query.where(User.name.ilike(f"%{name}%"))
        if surname:
            query = query.where(User.surname.ilike(f"%{surname}%"))
        if email:
            query = query.where(User.email.ilike(f"%{email}%"))

        result = await self.db.execute(query)
        return result.scalars().all()

    async def upcoming_birthdays(self):
        today = date.today()
        upcoming = today + timedelta(days=7)

        query = select(User).where(
            or_(
                and_(
                    extract("month", User.birthdate) == today.month,
                    extract("day", User.birthdate) >= today.day,
                    extract("day", User.birthdate) <= upcoming.day,
                ),
                and_(
                    extract("month", User.birthdate) == upcoming.month,
                    extract("day", User.birthdate) <= upcoming.day,
                ),
            )
        )

        result = await self.db.execute(query)
        return result.scalars().all()
