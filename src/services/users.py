from src.repository.users import UserRepository
from src.db.models import User
from src.api.exceptions import UserNotFoundError, DuplicateEmailError, ServerError


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_users(self, limit: int, skip: int):
        try:
            return await self.repo.get_all(limit=limit, skip=skip)
        except Exception as e:
            raise ServerError(str(e))

    async def get_user(self, user_id: int):
        try:
            user = await self.repo.get_by_id(user_id)
            if user is None:
                raise UserNotFoundError
            return user
        except UserNotFoundError:
            raise
        except Exception as e:
            raise ServerError(str(e))

    async def create_user(self, data):
        if await self.repo.get_by_email(data.email):
            raise DuplicateEmailError
        try:
            new_user = User(**data.dict())
            return await self.repo.create(new_user)
        except Exception as e:
            raise ServerError(str(e))

    async def update_user(self, user_id: int, data):
        existing = await self.repo.get_by_id(user_id)
        if not existing:
            raise UserNotFoundError
        if await self.repo.get_by_email(data.email) and existing.email != data.email:
            raise DuplicateEmailError
        try:
            return await self.repo.update(existing, data.dict())
        except Exception as e:
            raise ServerError(str(e))

    async def delete_user(self, user_id: int):
        existing = await self.repo.get_by_id(user_id)
        if not existing:
            raise UserNotFoundError
        try:
            await self.repo.delete(existing)
        except Exception as e:
            raise ServerError(str(e))

    async def search_users(self, name, surname, email):
        try:
            return await self.repo.search(name, surname, email)
        except Exception as e:
            raise ServerError(str(e))

    async def upcoming_birthdays(self):
        try:
            return await self.repo.upcoming_birthdays()
        except Exception as e:
            raise ServerError(str(e))
