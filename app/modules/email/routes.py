import logging

import aiosmtplib
from email.message import EmailMessage
from fastapi import APIRouter, Depends, status

from app.core.config import settings
from app.core.exceptions import BadRequest
from app.modules.auth.deps import get_current_user
from app.modules.email.schemas import SendEmailRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/send", status_code=status.HTTP_200_OK)
async def send_email(body: SendEmailRequest, current_user: dict = Depends(get_current_user)):
    if not settings.smtp_username or not settings.smtp_password:
        raise BadRequest("SMTP is not configured on the server")

    msg = EmailMessage()
    msg["From"] = settings.smtp_from_email or settings.smtp_username
    msg["To"] = body.to_email
    msg["Subject"] = body.subject
    msg.set_content(body.body)

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            ssl=True,
            username=settings.smtp_username,
            password=settings.smtp_password,
        )
    except Exception as e:
        logger.error("Email send error: %s", e)
        raise BadRequest(f"Failed to send email: {e}")

    return {"message": "Email sent successfully", "to": body.to_email}
