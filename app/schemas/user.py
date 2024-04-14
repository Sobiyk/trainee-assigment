from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    name: str | None = None
    surname: str | None = None
    role: str


class UserCreate(schemas.BaseUserCreate):
    name: str | None = None
    surname: str | None = None
    role: str
