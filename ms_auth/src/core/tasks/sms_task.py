import asyncio
from src.core.celery_app import celery_app
from src.core.external.sms_service_impl import create_sms_service


@celery_app.task(name="send_otp_code")
def send_otp_code_task(phone_number: str, code: str) -> None:
    sms_service = create_sms_service()
    asyncio.run(sms_service.send_otp(phone_number, code))
