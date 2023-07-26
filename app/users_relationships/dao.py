from app.dao.base import BaseDAO
from app.users_relationships.models import UserRelationship
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError
from app.users.models import User

from app.database import async_session_maker


class UserRelDAO(BaseDAO):
    model = UserRelationship


    @classmethod
    async def get_requests(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(User.user_name).where(User.id.in_(select(UserRelationship.user_to_id).filter_by(**filter_by)))
            result = await session.execute(query)
            return result.scalars().all()