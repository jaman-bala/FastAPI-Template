from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.domain.users import User


class UserRepository(BaseRepository):
    model = User


    async def get_by_phone(self, phone: str) -> User | None:
        query = select(self.model).where(self.model.phone == phone)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()