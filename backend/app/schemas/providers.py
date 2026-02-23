from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ProviderName = Literal["openai", "claude", "gemini"]
ProviderStatus = Literal["connected", "disconnected", "error", "disabled"]


class Provider(BaseModel):
    id: str
    name: ProviderName
    status: ProviderStatus
    lastError: str | None = None
    createdAt: datetime
    updatedAt: datetime


class ProvidersResponse(BaseModel):
    providers: list[Provider]


class CreateProviderRequest(BaseModel):
    name: ProviderName
    tokenRef: str = Field(min_length=1, max_length=200)


class UpdateProviderRequest(BaseModel):
    status: ProviderStatus


class ProviderResponse(BaseModel):
    provider: Provider
