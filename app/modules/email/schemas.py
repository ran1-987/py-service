from pydantic import BaseModel, EmailStr


class SendEmailRequest(BaseModel):
    to_email: EmailStr
    body: str
    subject: str = "Message from App"
