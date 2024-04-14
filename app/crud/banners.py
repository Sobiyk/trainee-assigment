from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banners import TagBanner

from .base import CRUDBase
from app.models import Banner, BannerContent, Feature, Tag

SELECT_BANNER = (
    select(Banner)
    .options(joinedload(Banner.content.and_(BannerContent.is_actual == True)))
    .options(selectinload(Banner.tags))
)


class CRUDBanner(CRUDBase):

    async def create(self, object_data: BaseModel, session: AsyncSession):
        object_data = object_data.model_dump()
        banner_content = object_data.pop('content', None)
        tags = object_data.pop('tag_ids', None)
        banner = Banner(**object_data)
        await self.check_uniqueness(tags, object_data['feature_id'], session)
        session.add(banner)
        await session.commit()

        for tag in tags:
            await tag_banner_crud.create(tag, banner.id, session)

        session.add(banner)
        banner_content = BannerContent(**banner_content)
        banner_content.banner_id = banner.id
        session.add(banner_content)
        await session.commit()
        stmt = SELECT_BANNER.where(Banner.id == banner.id)
        res = await session.execute(stmt)
        res = res.scalar()
        return res

    async def get_by_id(self, banner_id: int, session: AsyncSession):
        stmt = SELECT_BANNER.where(Banner.id == banner_id)
        banner = await session.execute(stmt)
        banner = banner.scalar()
        if banner is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Баннера с таким id не существует'
            )
        return banner

    async def get_multi(
            self,
            session: AsyncSession,
            tag_id: int = None,
            feature_id: int = None
    ):
        stmt = SELECT_BANNER
        if tag_id is not None:
            stmt = stmt.where(Banner.tags.any(Tag.id == tag_id))
        if feature_id is not None:
            stmt = stmt.where(Banner.feature_id == feature_id)
        all_objects = await session.execute(stmt)
        return all_objects.unique().scalars().all()

    async def get_by_tag_and_feature(
            self, tag_id: int, feature_id: int, session: AsyncSession
    ):
        await tag_crud.get(tag_id, session)
        await feature_crud.get(feature_id, session)

        db_obj = await session.execute(
            SELECT_BANNER
            .where(
                Banner.tags.any(Tag.id == tag_id),
                Banner.feature_id == feature_id,
                Banner.is_active == True)
            .join(Tag, Tag.id == tag_id)
        )
        obj = db_obj.scalar()
        return obj

    async def update(
            self, obj_in: BaseModel, db_obj: Banner, session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        content = update_data.pop('content', None)
        tags = update_data.pop('tag_ids', None)
        await self.check_uniqueness(tags, update_data['feature_id'], session)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if content is not None:
            stmt = (
                select(BannerContent)
                .where(
                    BannerContent.banner_id == db_obj.id,
                    BannerContent.is_actual == True)
            )
            old_content = await session.execute(stmt)
            old_content = old_content.scalar()
            old_content.is_actual = False
            session.add(old_content)
            new_content = BannerContent(**content)
            new_content.banner_id = db_obj.id
            session.add(new_content)
        if tags is not None:
            db_obj.tags = []
            for tag in tags:
                tag = await tag_crud.get(tag, session)
                db_obj.tags.append(tag)
        session.add(db_obj)
        await session.commit()
        return

    async def check_uniqueness(self, tags, feature_id, session: AsyncSession):
        sql_query = text(
            """
            SELECT b.id
            FROM banner AS b
            JOIN tagbanner AS tb ON b.id = tb.banner_id
            WHERE b.feature_id = :feature_id
            GROUP BY b.id
            HAVING array_agg(tb.tag_id ORDER BY tb.tag_id) = :tag_ids
            """
        )
        result = await session.execute(
            sql_query,
            {"feature_id": feature_id, "tag_ids": tags}
        )
        existing_banner = result.scalar_one_or_none()

        if existing_banner:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Баннер с таким набором тэгов и фич уже существует.'
            )


class CRUDTagBanner(CRUDBase):

    async def create(self, tag_id, banner_id, session: AsyncSession):
        data_in = {
            'tag_id': tag_id,
            'banner_id': banner_id
        }
        db_obj = TagBanner(**data_in)
        session.add(db_obj)
        try:
            await session.commit()
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.detail
            )


class CRUDBannerContent(CRUDBase):

    async def get_multi_by_banner_id(
        self,
        banner_id: int,
        session: AsyncSession
    ):
        stmt = (
            select(BannerContent).where(BannerContent.banner_id == banner_id)
        )
        result = await session.execute(stmt)
        result = result.scalars().all()
        return result

    async def activate_content(
        self,
        banner_id: int,
        content_id: int,
        session: AsyncSession
    ):
        not_actual_content: BannerContent = await self.get(content_id, session)
        stmt = (
            select(BannerContent)
            .where(
                BannerContent.banner_id == banner_id,
                BannerContent.is_actual == True
            )
        )
        actual_content = await session.execute(stmt)
        actual_content = actual_content.scalar()
        actual_content.is_actual = False
        not_actual_content.is_actual = True
        session.add(not_actual_content)
        session.add(actual_content)
        await session.commit()


banners_crud = CRUDBanner(Banner)
banner_content_crud = CRUDBannerContent(BannerContent)
tag_crud = CRUDBase(Tag)
feature_crud = CRUDBase(Feature)
tag_banner_crud = CRUDTagBanner(TagBanner)
