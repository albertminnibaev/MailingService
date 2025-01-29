from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ObjectDoesNotExist


class BaseCRUD:
    model = None

    @classmethod
    async def get_all(
            cls,
            db_session: AsyncSession,
            **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db_session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_one_or_none_by_id(
            cls,
            data_id: int,
            db_session: AsyncSession,
    ):
        obj = await db_session.get(cls.model, data_id)
        return obj

    @classmethod
    async def add(
            cls,
            data,
            db_session: AsyncSession,
    ):
        new_object = cls.model(**data.model_dump())
        db_session.add(new_object)
        try:
            await db_session.commit()
            await db_session.refresh(new_object)
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise e
        return new_object

    @classmethod
    async def update(
            cls,
            data_id: int,
            data,
            db_session: AsyncSession,
    ):
        old_object = await db_session.get(cls.model, data_id)
        if not old_object:
            raise ObjectDoesNotExist
        for key, value in data.model_dump().items():
            if value:
                setattr(old_object, key, value)
        await db_session.commit()
        await db_session.refresh(old_object)
        return old_object

    @classmethod
    async def delete(
            cls,
            data_id: int,
            db_session: AsyncSession,
    ):
        old_object = await db_session.get(cls.model, data_id)
        if not old_object:
            raise ObjectDoesNotExist
        await db_session.delete(old_object)
        await db_session.commit()
