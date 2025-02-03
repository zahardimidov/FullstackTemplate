from api.dependencies import CurrentUser
from api.users.schemas import *
from common.security import create_jwt_token, verify_password
from database.requests import *
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/user")


@router.post('/auth/sign-up', response_model=UserSignInResponse, status_code=200)
async def signup(data: UserSignUp):
    if await get_user_by_email(email=data.email):
        raise HTTPException(
            status_code=409, detail='Такой email уже зарегистрирован.')

    user: User = await create_user(**dict(
        name=data.name,
        email=data.email,
        password=data.password
    ))
    auth_token = create_jwt_token({"jwt_id": user.jwt_id})

    return dict(
        token=auth_token
    )


@router.post('/auth/sign-in', response_model=UserSignInResponse, status_code=200)
async def signin(data: UserSignIn):
    user = await get_user_by_email(email=data.email)

    if user is None or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401, detail='Неверный email или пароль.')

    auth_token = create_jwt_token(data={
        'jwt_id': user.jwt_id
    })

    return dict(
        token=auth_token
    )


@router.post('/me', response_model=UserMe, status_code=200)
async def me(user: CurrentUser):
    return user.to_dict()
