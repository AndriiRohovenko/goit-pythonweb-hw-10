from src.repository.users import UserRepository
from src.db.models import User
from src.api.exceptions import UserNotFoundError, DuplicateEmailError, ServerError
from src.schemas.auth import UserCreate


from libgravatar import Gravatar


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

    async def create_user(self, data: UserCreate):
        if await self.repo.get_by_email(data.email):
            raise DuplicateEmailError
        try:
            from src.api.utils import hash_password

            g = Gravatar(data.email)
            avatar = g.get_image()
            hashed_password = hash_password(data.password)

            user_data = data.model_dump(exclude={"password"})
            print(user_data)
            print("Type of data passed to repo.create:", type(data))

            return await self.repo.create(
                user_data, hashed_password=hashed_password, avatar=avatar
            )
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

    async def get_user_by_email(self, email: str):
        try:
            return await self.repo.get_by_email(email)
        except Exception as e:
            raise ServerError(str(e))
