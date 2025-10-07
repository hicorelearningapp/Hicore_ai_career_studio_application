import os
import random
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from .base import IOTPService, otp_storage

# Load .env
load_dotenv()

class EmailOTPService(IOTPService):
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 465))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")

    def send_otp(self, email: str) -> str:
        otp = str(random.randint(100000, 999999))
        otp_storage[email.lower()] = otp

        subject = "Your OTP Code"
        body = f"Your OTP code is: {otp}"

        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, email, message.as_string())

        print(f"[Email] OTP {otp} sent to {email}")
        return otp

    def verify_otp(self, email: str, otp: str) -> bool:
        return otp_storage.get(email.lower()) == otp
