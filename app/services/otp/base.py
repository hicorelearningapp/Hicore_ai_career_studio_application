from abc import ABC, abstractmethod

otp_storage = {}

class IOTPService(ABC):
    @abstractmethod
    def send_otp(self, identifier: str) -> str:
        pass

    @abstractmethod
    def verify_otp(self, identifier: str, otp: str) -> bool:
        pass
