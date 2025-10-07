from abc import ABC, abstractmethod
from app.models.user import User, RoleEnum

class IAuthService(ABC):
    @abstractmethod
    def login_or_register(self, role: RoleEnum, email: str = None, phone: str = None, otp: str = None) -> User:
        pass
