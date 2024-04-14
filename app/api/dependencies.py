from fastapi import Depends, HTTPException, status

from app.core.user import current_user
from app.models import User
from app.models.enums import UserRole


async def is_admin(user: User = Depends(current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас нет прав администратора',
        )
    return user
