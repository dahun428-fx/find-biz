from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    cause: str | None = None
