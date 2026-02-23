# Orchestration Plan (FE/BE)

## 1. 목표
- 프론트엔드와 백엔드의 책임 경계를 명확히 분리한다.
- API 계약 기반으로 병렬 개발한다.
- 설치 실행은 비동기 Job으로 오케스트레이션한다.

## 2. 팀 역할 (RACI)

## FE Team
- 책임(Responsible):
1. `/dashboard`, `/skills` UI 구현
2. 검색/필터/정렬/모달/챗봇 패널 UX
3. API 호출 상태(loading/error/empty) 처리
- 협의(Consulted):
1. 응답 스키마 변경 영향 검토

## BE Team
- 책임(Responsible):
1. DB 스키마 및 마이그레이션
2. API 구현(`/api/skills`, `/api/install-runs`, `/api/chat-ops`)
3. Job worker 및 provider adapter 구현
4. 권한/감사로그/에러코드 관리
- 협의(Consulted):
1. 화면별 필요한 집계 데이터 형태

## Tech Lead (or PM)
- 승인(Accountable):
1. API 계약/상태머신/스프린트 범위 승인
2. 릴리스 게이트 승인

---

## 3. 오케스트레이션 아키텍처
1. FE -> API 요청
2. API는 검증 후 Job 생성 (`202 Accepted`)
3. Worker가 provider adapter 호출
4. Run 상태 업데이트 (`queued/running/success/failed/partial_failed`)
5. FE가 polling/SSE로 상태 반영
6. 챗봇 명령도 동일 파이프라인 사용

---

## 4. 계약 중심 개발 규칙
1. 단일 계약 문서: `docs/05-api-contract.md`
2. 상태 표준 문서: `docs/06-job-lifecycle.md`
3. provider 표준 문서: `docs/07-provider-adapter-spec.md`
4. 계약 변경 시:
- 문서 변경 -> FE/BE 동시 리뷰 -> 구현 반영

---

## 5. 스프린트 백로그 (권장)

## Sprint 1 (기반)
### BE
1. `skills/providers/install_runs/chat_actions` 스키마 생성
2. `/api/skills` DB 연동
3. `/api/install-runs` (mock worker) 구현

### FE
1. `/skills` 목록/등록 UI
2. `/dashboard` KPI/최근 실행 UI
3. run 상태 폴링 훅 구현

### 완료 기준
- Skill 등록 후 목록 반영
- 설치 실행 요청 시 run이 `queued -> running -> success/failed`로 변함

## Sprint 2 (실행)
### BE
1. OpenAI adapter 연결
2. retry/rollback 액션 구현
3. 감사로그 저장

### FE
1. 설치/재시도/롤백 인터랙션 연결
2. 실패 상세/재시도 UX
3. 챗봇 패널 기본 명령 연결

### 완료 기준
- 단일 provider 실설치 성공
- 실패 재시도 동작
- 챗봇 명령으로 run 생성 가능

## Sprint 3 (확장)
### BE
1. Claude/Gemini adapter 추가
2. 부분 실패 집계 및 알림 규칙

### FE
1. provider별 상태 시각화 강화
2. 대시보드 알림/필터 고도화

### 완료 기준
- 멀티 provider 일괄 설치
- `partial_failed` 처리 및 UI 반영

---

## 6. 핸드오프 규칙
1. FE가 필요한 데이터 필드는 issue로 명시
2. BE는 샘플 응답(JSON fixture) 먼저 제공
3. QA 시나리오는 FE/BE 공동 유지

---

## 7. 릴리스 게이트
1. `pnpm lint`, `pnpm build` 통과
2. 핵심 API 테스트 통과
3. e2e 핵심 플로우 통과:
- Skill 등록
- 설치 실행
- 실패 재시도
- 상태 확인

---

## 8. 리스크와 대응
1. 리스크: provider별 API 차이
- 대응: adapter 인터페이스 고정 + 에러코드 정규화

2. 리스크: FE/BE 일정 불일치
- 대응: 계약 우선 + fixture 기반 병렬 개발

3. 리스크: 장시간 실행 상태 고착
- 대응: timeout + watchdog + 재시도 정책

