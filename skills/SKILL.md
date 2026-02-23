---
name: project-orchestrator
description: Use this skill when planning, implementing, or coordinating work in the find-biz repository. It defines canonical document priority, FE/BE orchestration flow, and markdown cleanup rules so work always follows the same source of truth.
---

# Project Orchestrator Skill

## When to use
- 이 저장소에서 기능 구현/설계/리뷰/핸드오프 작업을 할 때
- 어떤 문서를 기준으로 작업할지 혼선이 있을 때
- 문서가 중복되어 정리/통합이 필요할 때

## Step 0: 역할별 필수 참조 패킷
### 공통 패킷 (FE/BE 공통, 작업 시작 전 필수)
1. `skills/SKILL.md`
2. `docs/README.md`
3. `docs/00-code-rules.md`
4. `docs/05-api-contract.md`
5. `docs/06-job-lifecycle.md`
6. `docs/10-orchestration-plan.md`

### FE 패킷
1. `docs/frontend/00-frontend-playbook.md`
2. `docs/09-ui-design-spec.md`
3. `docs/01-ia-wireframe.md`
4. `docs/02-action-spec.md`
5. `nextjs-ai-chatbot/app/(platform)/dashboard/page.tsx`
6. `nextjs-ai-chatbot/app/(platform)/skills/page.tsx`

### BE 패킷
1. `docs/backend/01-backend-work-plan.md`
2. `docs/backend/02-feature-breakdown-and-flow.md`
3. `docs/04-domain-model.md`
4. `docs/07-provider-adapter-spec.md`
5. `docs/08-security-and-ops.md`
6. `backend/README.md`

## Step 1: Canonical 문서 로딩 순서
1. `docs/README.md`
2. `docs/00-code-rules.md`
3. `docs/04-domain-model.md`
4. `docs/05-api-contract.md`
5. `docs/06-job-lifecycle.md`
6. `docs/09-ui-design-spec.md`
7. `docs/10-orchestration-plan.md`

필요 시 팀별 문서:
- FE: `docs/frontend/00-frontend-playbook.md`
- BE: `docs/backend/01-backend-work-plan.md`, `docs/backend/02-feature-breakdown-and-flow.md`

## Step 2: 실행 오케스트레이션
1. 계약 고정:
- API/상태/어댑터 스펙부터 확정 (`05`, `06`, `07`)
2. 병렬 개발:
- FE는 화면/상태 처리, BE는 API/Worker/Adapter 구현
3. 연결 검증:
- run 상태 전이(`queued -> running -> success|failed|partial_failed`)가 UI에 반영되는지 확인
4. 릴리스 게이트:
- lint/build/test + 핵심 E2E 시나리오 확인

## Step 2.1: 오케스트레이터 지휘 프로토콜
1. 모든 작업 티켓에 "필수 참조 파일" 목록을 명시한다.
2. FE 티켓에는 상태값(`queued/running/success/failed/partial_failed`)과 필요한 API 필드를 함께 명시한다.
3. BE 티켓에는 요청/응답 예시(JSON)와 에러코드를 함께 명시한다.
4. API shape 변경은 코드 변경 전에 `docs/05-api-contract.md`를 먼저 수정한다.
5. 머지 전 `lint/build/test`와 계약 불일치 여부를 확인한다.

티켓 템플릿:
- FE: `skills/references/fe-ticket-template.md`
- BE: `skills/references/be-ticket-template.md`

## Step 3: 문서 관리 규칙
1. 구현 기준은 `docs/` 하위 canonical 문서만 사용
2. 중복/레거시 문서는 `docs/archive/`로 이동
3. 링크가 깨지면 같은 작업에서 즉시 수정
4. 문서 정리 결과는 `docs/11-md-inventory-and-cleanup.md`에 기록

## Step 3.1: 금지 규칙
1. `docs/archive/*` 문서를 구현 기준으로 사용하지 않는다.
2. 구두 합의만으로 API/상태값/에러코드를 변경하지 않는다.
3. FE/BE 중 한쪽만 아는 상태값/필드를 추가하지 않는다.

## Quick checklist
- [ ] 변경 전 `docs/README.md`에서 기준 문서 확인
- [ ] 구현이 `00-code-rules`와 `05-api-contract`를 위반하지 않는지 확인
- [ ] 새 작업이 FE/BE 어디 책임인지 `10-orchestration-plan` 기준으로 분리
- [ ] 문서 중복 생성 없이 기존 문서에 통합

## Reference map
- `skills/references/doc-map.md`
