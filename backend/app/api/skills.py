from fastapi import APIRouter, Query

from app.schemas.skills import CreateSkillRequest, CreateSkillResponse, SkillsResponse
from app.services.store import store

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=SkillsResponse)
def list_skills(search: str | None = None, limit: int = Query(default=20, ge=1, le=100)) -> SkillsResponse:
    return SkillsResponse(skills=store.list_skills(search=search, limit=limit))


@router.post("", response_model=CreateSkillResponse, status_code=201)
def create_skill(payload: CreateSkillRequest) -> CreateSkillResponse:
    skill = store.create_skill(
        title=payload.title,
        description=payload.description,
        github_url=str(payload.githubUrl),
        tags=payload.tags,
    )
    return CreateSkillResponse(skill=skill)
