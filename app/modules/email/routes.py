import logging

import requests
from fastapi import APIRouter, Depends, status

from app.core.config import settings
from app.core.exceptions import BadRequest
from app.modules.auth.deps import get_current_user
from app.modules.email.schemas import SendEmailRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/send", status_code=status.HTTP_200_OK)
async def send_email(body: SendEmailRequest, current_user: dict = Depends(get_current_user)):
    if not settings.mailgun_api_key or not settings.mailgun_domain:
        raise BadRequest("Mailgun is not configured on the server")

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{settings.mailgun_domain}/messages",
            auth=("api", settings.mailgun_api_key),
            data={
                "from": settings.mailgun_from_email,
                "to": body.to_email,
                "subject": body.subject,
                "text": body.body,
            },
        )
        response.raise_for_status()
    except Exception as e:
        logger.error("Email send error: %s", e)
        raise BadRequest(f"Failed to send email: {e}")

    return {"message": "Email sent successfully", "to": body.to_email}
