from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import BaseIntPK
from app.models.enums import UserRole


class User(SQLAlchemyBaseUserTable[int], BaseIntPK):
    name: Mapped[str | None] = mapped_column(String(64))
    surname: Mapped[str | None] = mapped_column(String(64))
    role: Mapped[UserRole] = mapped_column(server_default='basic')
