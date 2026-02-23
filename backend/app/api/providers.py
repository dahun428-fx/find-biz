from fastapi import APIRouter

from app.core.errors import raise_api_error
from app.schemas.providers import (
    CreateProviderRequest,
    ProviderResponse,
    ProvidersResponse,
    UpdateProviderRequest,
)
from app.services.store import store

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=ProvidersResponse)
def list_providers() -> ProvidersResponse:
    return ProvidersResponse(providers=store.list_providers())


@router.post("", response_model=ProviderResponse, status_code=201)
def create_provider(payload: CreateProviderRequest) -> ProviderResponse:
    provider = store.create_provider(name=payload.name)
    return ProviderResponse(provider=provider)


@router.patch("/{provider_id}", response_model=ProviderResponse)
def update_provider(provider_id: str, payload: UpdateProviderRequest) -> ProviderResponse:
    provider = store.update_provider_status(provider_id=provider_id, status=payload.status)
    if provider is None:
        raise_api_error(404, "not_found:provider", "Provider not found")
    return ProviderResponse(provider=provider)
