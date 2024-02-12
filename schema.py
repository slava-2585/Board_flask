from abc import ABC
from typing import Optional

import pydantic


class AbstractUser(pydantic.BaseModel, ABC):
    name: str
    email: str
    password: str

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f"Minimal length of password is 8")
        return v


class AbstractAdv(pydantic.BaseModel, ABC):
    title: str
    description: str


class CreateUser(AbstractUser):
    name: str
    password: str


class UpdateAdv(AbstractAdv):
    title: Optional[str] = None
    description: Optional[str] = None


class CreateAdv(AbstractAdv):
    title: str
    description: str
