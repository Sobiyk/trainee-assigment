from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    name: str | None
    surname: str | None
    role: str


class UserCreate(schemas.BaseUserCreate):
    name: str | None
    surname: str | None
