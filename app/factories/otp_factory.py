from app.services.otp.sms_service import SMSOTPService
from app.services.otp.email_service import EmailOTPService
from app.services.otp.base import IOTPService

class OTPFactory:
    @staticmethod
    def get_service(identifier: str) -> IOTPService:
        if "@" in identifier:
            return EmailOTPService()
        else:
            return SMSOTPService()
