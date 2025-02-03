import re

from common.schemas import BaseModel, CustomStr, PydanticBaseModel
from pydantic import model_validator
from typing_extensions import Self


def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


class Email(CustomStr):
    @classmethod
    def validate(cls, value):
        if not 8 <= len(value) <= 120:
            raise ValueError

        if not validate_email(value):
            raise ValueError

        return value


class Password(CustomStr):
    @classmethod
    def validate(cls, value):
        if not 8 <= len(value) <= 60:
            raise ValueError

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value):
            raise ValueError
        return value


class UserSignUp(BaseModel):
    name: str
    email: Email

    password: Password
    password_repeat: Password

    @model_validator(mode='after')
    def full_validation(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError
        return self


class UserSignIn(BaseModel):
    email: Email
    password: Password


class UserSignInResponse(BaseModel):
    token: str


class UserMe(PydanticBaseModel):
    name: str
    email: Email
