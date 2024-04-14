import datetime
from pydantic import BaseModel, ConfigDict, Field

from .metaclass import AllFieldsOptionalModel


class BannerContentCreate(BaseModel):
    title: str
    text: str
    url: str


class BannerCreate(BaseModel):
    tag_ids: list[int]
    feature_id: int
    content: BannerContentCreate


class BannerCreateOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., alias='banner_id')


class BannerContentOut(BannerContentCreate):
    pass


class BannerContentHistoryOut(BannerContentOut):
    id: int
    is_actual: bool


class BannerOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True
    )

    id: int = Field(..., alias='banner_id')
    tag_ids: list[int]
    feature_id: int
    content: BannerContentOut
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class BannerUpdate(BannerCreate, AllFieldsOptionalModel):
    pass
