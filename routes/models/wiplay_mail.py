from pydantic import BaseModel
from typing_extensions import Annotated
from fastapi import Form

class WiplayEmail(BaseModel):
    """Request model for the Wiplay
    e-mails."""
    args: Annotated[str, Form()]
    destinatary: Annotated[str, Form()]
    subject: Annotated[str, Form()]
