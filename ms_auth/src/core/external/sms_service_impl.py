import logging
from src.domain.services.sms_service import ISMSService
from src.config import settings
import aiohttp

logger = logging.getLogger(__name__)

class MockSMSService(ISMSService):
    async def send_otp(self, phone_number: str, code: str) -> None:
        logger.info(f"[MOCK SMS] To {phone_number}: your OTP is {code}")

class TelegramSMSService(ISMSService):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    async def send_otp(self, phone_number: str, code: str) -> None:
        message_text = f"OTP code: `{code}`\nfor phone number: `{phone_number}`"
        payload = {
            "chat_id": settings.chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, jspn=payload) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        logger.error(f"erorr: {resp.status}: {error_text}")
                    else:
                        logger.info(f"OTP {code} sent to tg chat {self.chat_id}")
        except Exception as e:
            logger.exception(f"failed to send telegram to tg chat {e}")

def create_sms_service() -> ISMSService:
    if settings.SMS_PROVIDER == "mock":
        return MockSMSService()
    elif settings.SMS_PROVIDER == "telegram":
        return TelegramSMSService(
            bot_token=settings.TELEGRAM_BOT_TOKEN,
            chat_id=settings.TELEGRAM_CHAT_ID,
        )
    else:
        raise ValueError(f"Unknown sms provider: [{settings.SMS_PROVIDER}]")
