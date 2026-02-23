# Markdown Inventory & Cleanup Report

## 목적
- 프로젝트 내 `.md` 문서를 전수 확인하고, canonical/legacy를 분류해 정리 상태를 기록한다.

## 스캔 결과
- 총 `.md` 파일: 34개
- 주요 그룹:
1. 현재 기준 문서: `docs/` + `docs/frontend/` + `docs/backend/`
2. 템플릿 문서: `nextjs-ai-chatbot/README.md`
3. 백엔드 런타임 안내: `backend/README.md`
4. 레거시/중복 문서: `regacy-docs/*`, `backend/docs/*`

## 분류 정책
### Canonical (구현 기준)
- `docs/README.md`에 등록된 문서

### Archive (보관)
- `docs/archive/regacy-docs/SUMMARY.md`
- `docs/archive/backend-docs/SUMMARY.md`

## 이번 정리 작업
1. `regacy-docs/` -> `docs/archive/regacy-docs/`로 이동
2. `backend/docs/` -> `docs/archive/backend-docs/`로 이동
3. 참조 경로 업데이트:
  - `docs/frontend/README.md`
4. canonical 인덱스 생성:
  - `docs/README.md`
5. archive 정책 문서 생성:
  - `docs/archive/README.md`

## 2차 정리 작업
1. 아카이브 상세 문서를 요약본으로 통합:
  - `docs/archive/regacy-docs/SUMMARY.md`
  - `docs/archive/backend-docs/SUMMARY.md`
2. 아카이브의 개별 중복 `.md` 원문 삭제
3. 아카이브 정책 문서에 "요약본 유지" 원칙 반영

## 3차 정리 작업
1. `docs/frontend/` 분산 문서 6개를 단일 문서로 통합:
  - `docs/frontend/00-frontend-playbook.md`
2. 기존 분산 문서 삭제:
  - `01-frontend-work-plan.md`
  - `02-api-integration-checklist.md`
  - `03-qa-release-checklist.md`
  - `04-backend-handoff-requirements.md`
  - `05-backend-ticket-breakdown.md`
  - `06-frontend-implementation-plan.md`
3. 아카이브 요약 추가:
  - `docs/archive/frontend-docs/SUMMARY.md`
4. 인덱스 갱신:
  - `docs/README.md`
  - `docs/frontend/README.md`

## 후속 관리 규칙
1. 새 문서 생성 전 `docs/README.md`의 기존 문서 확장 가능성부터 확인
2. 중복 문서는 신규 작성 대신 기존 문서 섹션 추가로 통합
3. 작업 완료 후 깨진 참조 링크(`rg`) 점검
