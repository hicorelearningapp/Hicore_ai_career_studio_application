import os
import random
from twilio.rest import Client
from dotenv import load_dotenv
from app.services.otp.base import IOTPService
from app.services.auth.otp_service import otp_storage

# Load .env
load_dotenv()

class SMSOTPService(IOTPService):
    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.from_number = os.getenv("TWILIO_FROM_NUMBER")

    def send_otp(self, phone: str) -> str:
        otp = str(random.randint(100000, 999999))
        otp_storage[phone] = otp

        self.client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=self.from_number,
            to=phone
        )

        print(f"[SMS] OTP {otp} sent to {phone}")
        return otp

    def verify_otp(self, phone: str, otp: str) -> bool:
        return otp_storage.get(phone) == otp
