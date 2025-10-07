# app/factories/auth_factory.py
from app.repositories.user_repository import UserRepository
# from app.services.auth.google_service import GoogleAuthService
#from app.services.auth.linkedin_service import LinkedInAuthService
from app.services.auth.otp_service import OTPAuthService
from app.factories.otp_factory import OTPFactory

class AuthFactory:
    @staticmethod
    def get_service(provider: str, repo: UserRepository, identifier: str = None):
        if provider == "google":
            # return GoogleAuthService(repo)
            return "google"
        elif provider == "linkedin":
            # return LinkedInAuthService(repo)
            return "Linkedin"
        elif provider == "otp":
            if not identifier:
                raise ValueError("Identifier (email/phone) required for OTP provider")
            otp_service = OTPFactory.get_service(identifier)
            return OTPAuthService(repo, otp_service)
        else:
            raise ValueError("Unsupported provider")
