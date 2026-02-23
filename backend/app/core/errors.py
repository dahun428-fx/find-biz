from dataclasses import dataclass

from fastapi import HTTPException


@dataclass(frozen=True)
class ApiError:
    code: str
    message: str
    cause: str | None = None



def raise_api_error(status_code: int, code: str, message: str, cause: str | None = None) -> None:
    detail = {"code": code, "message": message}
    if cause:
        detail["cause"] = cause
    raise HTTPException(status_code=status_code, detail=detail)
