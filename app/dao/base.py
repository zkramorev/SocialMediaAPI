from sqlalchemy import delete, insert, select

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def add_new_one(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_one(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_all(cls, selected_columns=None, **filter_by):
        async with async_session_maker() as session:
            if selected_columns is None:
                query = select(cls.model.__table__.columns).filter_by(**filter_by)
            else:
                query = select(
                    cls.model.__table__.columns[*selected_columns]
                ).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
