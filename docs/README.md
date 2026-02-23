# Documentation Index (Canonical)

이 폴더는 프로젝트의 **단일 기준 문서(Source of Truth)** 입니다.  
구현/리뷰/운영 작업은 이 인덱스 순서로 참조합니다.

## 1) 규칙/아키텍처 (항상 먼저)
1. `docs/00-code-rules.md`
2. `docs/04-domain-model.md`
3. `docs/05-api-contract.md`
4. `docs/06-job-lifecycle.md`
5. `docs/07-provider-adapter-spec.md`
6. `docs/08-security-and-ops.md`

## 2) 화면/실행 계획
1. `docs/01-ia-wireframe.md`
2. `docs/02-action-spec.md`
3. `docs/03-mvp-checklist.md`
4. `docs/09-ui-design-spec.md`
5. `docs/10-orchestration-plan.md`

## 3) 팀별 실행 문서
- Backend:
  - `docs/backend/01-backend-work-plan.md`
  - `docs/backend/02-feature-breakdown-and-flow.md`
- Frontend:
- `docs/frontend/README.md`
- `docs/frontend/00-frontend-playbook.md`

## 4) 정리 원칙
1. 루트/다른 폴더의 중복 `.md`는 `docs/archive/`로 이동한다.
2. 구현 기준은 반드시 `docs/` 하위의 canonical 문서만 사용한다.
3. 문서 변경 시 관련 참조 링크를 같은 PR에서 함께 수정한다.

## 5) 아카이브
- 과거 기획/중복 문서는 `docs/archive/README.md`를 기준으로 보관한다.
