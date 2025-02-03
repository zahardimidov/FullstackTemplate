from typing import Annotated

from database.requests import get_one_by_jwt_id
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database.models import User
from common.security import verify_jwt_token

auth_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    decoded_data = verify_jwt_token(token.credentials)
    if not decoded_data:
        raise HTTPException(
            status_code=401, detail="Пользователь не авторизован.")

    user = await get_one_by_jwt_id(decoded_data["jwt_id"], User)
    if not user:
        raise HTTPException(
            status_code=401, detail="Пользователь не авторизован.")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]