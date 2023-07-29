from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import User
from app.users_relationships.models import UserRelationship


class UserRelDAO(BaseDAO):
    model = UserRelationship

    @classmethod
    async def get_requests(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(User.user_name).where(
                User.id.in_(select(UserRelationship.user_to_id).filter_by(**filter_by))
            )
            result = await session.execute(query)
            return result.scalars().all()
