from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class Skill(BaseModel):
    id: str
    title: str
    description: str
    githubUrl: HttpUrl
    tags: list[str]
    ownerId: str
    createdAt: datetime
    updatedAt: datetime


class SkillsResponse(BaseModel):
    skills: list[Skill]


class CreateSkillRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=1000)
    githubUrl: HttpUrl
    tags: list[str] = Field(default_factory=list, max_length=20)


class CreateSkillResponse(BaseModel):
    skill: Skill
