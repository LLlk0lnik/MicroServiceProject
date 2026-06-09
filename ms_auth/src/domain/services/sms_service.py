from abc import ABC, abstractmethod


class ISMSService(ABC):
    @abstractmethod
    async def send_otp(self, phone_number: str, code: str) -> None:
        pass
