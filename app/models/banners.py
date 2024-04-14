import datetime as dt

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.db import Base, BaseIntPK


class Tag(BaseIntPK):
    banners: Mapped[list['Banner']] = relationship(
        back_populates='tags', secondary='tagbanner', lazy='raise'
    )
    name: Mapped[str] = mapped_column(String(128), unique=True)


class TagBanner(Base):
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tag.id', ondelete='CASCADE'),
        primary_key=True
    )
    banner_id: Mapped[int] = mapped_column(
        ForeignKey('banner.id', ondelete='CASCADE'),
        primary_key=True
    )


class Feature(BaseIntPK):
    name: Mapped[str] = mapped_column(String(128), unique=True)


class Banner(BaseIntPK):
    tags: Mapped[list['Tag']] = relationship(
        back_populates='banners', secondary='tagbanner', lazy='raise'
    )
    feature_id: Mapped[int] = mapped_column(ForeignKey('feature.id'))
    is_active: Mapped[bool]
    created_at: Mapped[dt.datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        server_default=func.now(),
        server_onupdate=func.now()
    )
    content: Mapped['BannerContent'] = relationship(
        'BannerContent', lazy='raise', cascade="all, delete-orphan"
    )

    @hybrid_property
    def tag_ids(self):
        return [tag.id for tag in self.tags]


class BannerContent(BaseIntPK):
    title: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(String(256))
    url: Mapped[str]
    banner_id: Mapped[int | None] = mapped_column(
        ForeignKey('banner.id', ondelete='CASCADE')
    )
    is_actual: Mapped[bool] = mapped_column(default=True)
