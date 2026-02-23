# BE Ticket Template

## 제목
`[BE][우선순위] 기능명`

## 목적
- 비즈니스/운영 목적을 1~2문장으로 작성

## 필수 참조 파일
1. `docs/backend/01-backend-work-plan.md`
2. `docs/backend/02-feature-breakdown-and-flow.md`
3. `docs/04-domain-model.md`
4. `docs/05-api-contract.md`
5. `docs/06-job-lifecycle.md`
6. `docs/07-provider-adapter-spec.md`
7. `docs/00-code-rules.md`

## 범위
- 포함:
  - 
- 제외:
  - 

## API 계약 (필수)
- Endpoint:
- Request schema:
- Response schema:
- Error codes:
- Status code:

## 데이터/상태 규칙 (필수)
- Domain entity:
- Job 상태 전이:
  - `queued -> running -> success|failed|partial_failed`
- Retry/timeout:
- Idempotency key:

## 구현 대상 파일
- `backend/app/api/...`
- `backend/app/services/...`
- `backend/app/models/...`
- `backend/app/workers/...`

## 완료 기준 (AC)
1. 
2. 
3. 

## 테스트/검증
- [ ] 단위 테스트
- [ ] 통합 테스트
- [ ] 오류 케이스 테스트(최소 2개)
- [ ] `ruff check` / `ruff format` / `mypy`(적용 범위)

## 보안/운영 체크
- [ ] 민감정보 마스킹
- [ ] 감사로그 필드 기록
- [ ] 에러 포맷 `{code,message,cause?}` 일관성

## 의존성 / 블로커
- FE 영향:
- 선행 티켓:

## 산출물
- PR 링크:
- 샘플 응답(JSON):
- 문서 업데이트:

