from fastapi import APIRouter

from app.schemas.chat_ops import ChatOpsRequest, ChatOpsResponse, ResolvedAction
from app.services.store import store

router = APIRouter(prefix="/chat-ops", tags=["chat-ops"])


@router.post("", response_model=ChatOpsResponse)
def chat_ops(payload: ChatOpsRequest) -> ChatOpsResponse:
    text = payload.input.strip().lower()
    if "설치" not in text and "install" not in text:
        return ChatOpsResponse(intent="unknown", accepted=False, reason="설치 명령을 인식하지 못했습니다.")

    skills = store.list_skills(search=None, limit=1)
    providers = store.list_providers()
    if not skills:
        return ChatOpsResponse(intent="bulk_install", accepted=False, reason="등록된 skill이 없습니다.")
    if not providers:
        return ChatOpsResponse(intent="bulk_install", accepted=False, reason="연결된 provider가 없습니다.")

    skill = skills[0]
    provider_ids = [p.id for p in providers]
    created = store.create_runs(
        skill_id=skill.id,
        provider_ids=provider_ids,
        action="install",
    )
    return ChatOpsResponse(
        intent="bulk_install",
        resolvedAction=ResolvedAction(skillId=skill.id, providerScope="all", action="install", ref="main"),
        accepted=True,
        runIds=[r.id for r in created],
    )
