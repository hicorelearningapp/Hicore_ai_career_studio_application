from fastapi import HTTPException, status
from app.models.user import User, RoleEnum
from app.repositories.user_repository import UserRepository
from app.services.otp.base import IOTPService, otp_storage
from .base import IAuthService


class OTPAuthService(IAuthService):
    def __init__(self, repo: UserRepository, otp_service: IOTPService):
        self.repo = repo
        self.otp_service = otp_service

    def send_otp(self, identifier: str) -> str:
        """
        Delegates OTP generation & sending to the configured OTP service
        (e.g., SMS, Email).
        """
        return self.otp_service.send_otp(identifier)

    def verify_otp(self, identifier: str, otp: str) -> bool:
        """
        Delegates OTP verification to the configured OTP service.
        """
        return self.otp_service.verify_otp(identifier, otp)

    def login_or_register(
        self, role: RoleEnum, email: str = None, phone: str = None, otp: str = None
    ) -> User:
        identifier = phone or email
        if not self.verify_otp(identifier, otp):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )

        user = self.repo.find_by_email_or_phone(email, phone)
        if user:
            return user

        return self.repo.create_user(
            role=role,
            provider="otp",
            email=email,
            phone=phone
        )
