from abc import ABC, abstractmethod
from typing import Optional


class AccountRepositoryInterface(ABC):
    @abstractmethod
    async def save_user(self, username: str, password: str, email: Optional[str]): pass

    @abstractmethod
    async def get_user_by(self, username: str): pass
