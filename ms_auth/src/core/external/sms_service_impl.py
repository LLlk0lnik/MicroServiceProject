import logging
from src.domain.services.sms_service import ISMSService
from src.config import settings

logger = logging.getLogger(__name__)


class MockSMSService(ISMSService):
    async def send_otp(self, phone_number: str, code: str) -> None:
        logger.info(f"[MOCK SMS] To {phone_number}: your OTP is {code}")


def create_sms_service() -> ISMSService:
    if settings.SMS_PROVIDER == "mock":
        return MockSMSService()
    else:
        return ValueError(f"Unknown sms provider: [{settings.SMS_PROVIDER}]")
