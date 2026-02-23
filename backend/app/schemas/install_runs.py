from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

RunStatus = Literal["queued", "running", "success", "failed", "partial_failed"]
RunAction = Literal["install", "sync", "retry", "rollback"]


class InstallRun(BaseModel):
    id: str
    skillId: str
    providerId: str
    action: RunAction
    status: RunStatus
    attempt: int
    errorCode: str | None = None
    errorMessage: str | None = None
    startedAt: datetime | None = None
    finishedAt: datetime | None = None


class CreateInstallRunsRequest(BaseModel):
    action: RunAction
    skillId: str
    providerIds: list[str] = Field(min_length=1)
    requestedRef: str = "main"


class CreateInstallRunsResponse(BaseModel):
    runIds: list[str]
    status: RunStatus


class InstallRunsResponse(BaseModel):
    runs: list[InstallRun]
