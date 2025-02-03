import uuid
from datetime import datetime
from typing import Any, Dict

from common.security import hash_password
from sqlalchemy import TIMESTAMP, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def generate_uuid():
    return str(uuid.uuid4())


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String, default=generate_uuid, primary_key=True, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AuthModel(Base):
    __abstract__ = True

    email = mapped_column(String(120), nullable=False)
    _password = mapped_column("password", String(100), nullable=False)

    jwt_id = mapped_column(String, default=generate_uuid,
                           unique=True, nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = hash_password(value)


class User(AuthModel):
    __tablename__ = 'users'

    name = mapped_column(String(30), nullable=False)


class Product(Base):
    __tablename__ = 'products'

    name = mapped_column(String(50), nullable=False)
    price = mapped_column(Integer, nullable=False)
