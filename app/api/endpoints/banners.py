from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import is_admin
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.banners import banners_crud, banner_content_crud
from app.schemas.banners import (
    BannerContentHistoryOut,
    BannerCreate,
    BannerCreateOut,
    BannerOut,
    BannerUpdate
)

router = APIRouter()


@router.get(
    '/banner/',
    response_model=list[BannerOut],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(is_admin)]
)
async def get_banners(
    tag_id: int = None,
    feature_id: int = None,
    session: AsyncSession = Depends(get_async_session)
):
    return await banners_crud.get_multi(
        session, tag_id=tag_id, feature_id=feature_id
    )


@router.get(
    '/user_banner/',
    response_model=BannerOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_user)]
)
@cache(expire=300)
async def get_user_banner(
    tag_id: int,
    feature_id: int,
    use_last_revision: bool = False,
    session: AsyncSession = Depends(get_async_session)
):
    banner = await banners_crud.get_by_tag_and_feature(
        tag_id, feature_id, session)
    if banner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Баннер не найден'
        )
    return banner


@router.post(
    '/banner/',
    response_model=BannerCreateOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(is_admin)]
)
async def create_banner(
    object_data: BannerCreate,
    session: AsyncSession = Depends(get_async_session)
):
    res = await banners_crud.create(object_data, session)
    return res


@router.patch(
    '/banner/{id}/',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(is_admin)]
)
async def update_banner(
    id: int,
    update_data: BannerUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    banner = await banners_crud.get_by_id(id, session)
    await banners_crud.update(update_data, banner, session)
    return


@router.delete(
    '/banner/{id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(is_admin)]
)
async def remove_banner(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    banner = await banners_crud.get_by_id(id, session)
    return await banners_crud.remove(banner, session)


@router.get(
    '/banner/{id}/content/',
    response_model=list[BannerContentHistoryOut],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(is_admin)]
)
async def get_banner_history(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    banner_history = await banner_content_crud.get_multi_by_banner_id(
        id, session
    )
    return banner_history


@router.get(
    '/banner/{id}/content/{content_id}/activate/',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(is_admin)]
)
async def activate_content(
    id: int,
    content_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return await banner_content_crud.activate_content(id, content_id, session)
