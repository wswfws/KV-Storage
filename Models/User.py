import hashlib
from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class User:
    user_id: str
    password_hash: str

    def get_user_filename(self) -> str:
        return hashlib.sha256(self.user_id.encode()).hexdigest()


class UserModel(BaseModel):
    user_id: str = Field(default="", max_length=50)
    password_hash: str = Field(default="", min_length=64, max_length=64)

def convert_user_model_to_user(user_model: UserModel) -> User:
    """
    Конвертирует объект UserModel в объект User.

    :param user_model: Экземпляр модели UserModel
    :return: Экземпляр класса User
    """
    return User(user_id=user_model.user_id, password_hash=user_model.password_hash)
