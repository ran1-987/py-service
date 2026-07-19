import logging

from fastapi import APIRouter, Depends, status
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import settings
from app.core.exceptions import BadRequest
from app.modules.auth.deps import get_current_user
from app.modules.email.schemas import SendEmailRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/send", status_code=status.HTTP_200_OK)
async def send_email(body: SendEmailRequest, current_user: dict = Depends(get_current_user)):
    if not settings.sendgrid_api_key:
        raise BadRequest("SendGrid is not configured on the server")

    message = Mail(
        from_email=settings.sendgrid_from_email,
        to_emails=body.to_email,
        subject=body.subject,
        plain_text_content=body.body,
    )

    try:
        client = SendGridAPIClient(settings.sendgrid_api_key)
        client.send(message)
    except Exception as e:
        logger.error("Email send error: %s", e)
        raise BadRequest(f"Failed to send email: {e}")

    return {"message": "Email sent successfully", "to": body.to_email}
