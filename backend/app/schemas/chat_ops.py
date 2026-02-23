from typing import Literal

from pydantic import BaseModel


class ChatOpsRequest(BaseModel):
    input: str


class ResolvedAction(BaseModel):
    skillId: str
    providerScope: str
    action: Literal["install", "sync", "retry", "rollback"]
    ref: str = "main"


class ChatOpsResponse(BaseModel):
    intent: str
    resolvedAction: ResolvedAction | None = None
    accepted: bool
    runIds: list[str] = []
    reason: str | None = None
