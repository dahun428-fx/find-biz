from typing import Literal

from fastapi import APIRouter, Query

from app.schemas.install_runs import CreateInstallRunsRequest, CreateInstallRunsResponse, InstallRunsResponse
from app.services.store import store

router = APIRouter(prefix="/install-runs", tags=["install-runs"])

RunStatusParam = Literal["queued", "running", "success", "failed", "partial_failed"]


@router.post("", response_model=CreateInstallRunsResponse, status_code=202)
def create_install_runs(payload: CreateInstallRunsRequest) -> CreateInstallRunsResponse:
    runs = store.create_runs(skill_id=payload.skillId, provider_ids=payload.providerIds, action=payload.action)
    return CreateInstallRunsResponse(runIds=[r.id for r in runs], status="queued")


@router.get("", response_model=InstallRunsResponse)
def list_install_runs(
    skillId: str | None = None,
    providerId: str | None = None,
    status: RunStatusParam | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> InstallRunsResponse:
    runs = store.list_runs(skill_id=skillId, provider_id=providerId, status=status, limit=limit)
    return InstallRunsResponse(runs=runs)
