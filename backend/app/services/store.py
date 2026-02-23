from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import Lock
from uuid import uuid4

from app.schemas.install_runs import InstallRun, RunAction
from app.schemas.providers import Provider, ProviderName, ProviderStatus
from app.schemas.skills import Skill


@dataclass
class InMemoryStore:
    lock: Lock = field(default_factory=Lock)
    skills: dict[str, Skill] = field(default_factory=dict)
    providers: dict[str, Provider] = field(default_factory=dict)
    runs: dict[str, InstallRun] = field(default_factory=dict)

    def now(self) -> datetime:
        return datetime.now(UTC)

    def _id(self) -> str:
        return str(uuid4())

    def create_skill(self, title: str, description: str, github_url: str, tags: list[str]) -> Skill:
        with self.lock:
            now = self.now()
            skill = Skill(
                id=self._id(),
                title=title,
                description=description,
                githubUrl=github_url,
                tags=tags,
                ownerId="local-dev-owner",
                createdAt=now,
                updatedAt=now,
            )
            self.skills[skill.id] = skill
            return skill

    def list_skills(self, search: str | None, limit: int) -> list[Skill]:
        with self.lock:
            items = list(self.skills.values())
            if search:
                needle = search.lower()
                items = [s for s in items if needle in s.title.lower() or needle in s.description.lower()]
            return sorted(items, key=lambda s: s.createdAt, reverse=True)[:limit]

    def create_provider(self, name: ProviderName) -> Provider:
        with self.lock:
            now = self.now()
            provider = Provider(
                id=self._id(),
                name=name,
                status="connected",
                lastError=None,
                createdAt=now,
                updatedAt=now,
            )
            self.providers[provider.id] = provider
            return provider

    def list_providers(self) -> list[Provider]:
        with self.lock:
            return sorted(self.providers.values(), key=lambda p: p.createdAt, reverse=True)

    def update_provider_status(self, provider_id: str, status: ProviderStatus) -> Provider | None:
        with self.lock:
            provider = self.providers.get(provider_id)
            if provider is None:
                return None
            provider.status = status
            provider.updatedAt = self.now()
            self.providers[provider_id] = provider
            return provider

    def create_runs(self, skill_id: str, provider_ids: list[str], action: RunAction) -> list[InstallRun]:
        with self.lock:
            new_runs: list[InstallRun] = []
            for provider_id in provider_ids:
                run = InstallRun(
                    id=self._id(),
                    skillId=skill_id,
                    providerId=provider_id,
                    action=action,
                    status="queued",
                    attempt=1,
                    startedAt=None,
                    finishedAt=None,
                )
                self.runs[run.id] = run
                new_runs.append(run)
            return new_runs

    def list_runs(self, skill_id: str | None, provider_id: str | None, status: str | None, limit: int) -> list[InstallRun]:
        with self.lock:
            items = list(self.runs.values())
            if skill_id:
                items = [r for r in items if r.skillId == skill_id]
            if provider_id:
                items = [r for r in items if r.providerId == provider_id]
            if status:
                items = [r for r in items if r.status == status]
            items.sort(key=lambda r: (r.startedAt or r.finishedAt or self.now()), reverse=True)
            return items[:limit]


store = InMemoryStore()
