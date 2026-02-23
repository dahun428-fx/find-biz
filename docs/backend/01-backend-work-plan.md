# Backend Work Plan

## 1. 목적
- `docs/10-orchestration-plan.md`를 기준으로 백엔드 실행 계획을 구체화한다.
- FE와 계약 기반 병렬 개발이 가능하도록 API/상태/어댑터 구현 순서를 확정한다.
- 설치 실행을 비동기 Job 파이프라인으로 표준화한다.

## 2. 범위
- DB 스키마/마이그레이션
- API 구현 (`/api/skills`, `/api/install-runs`, `/api/chat-ops`)
- Job Worker + Provider Adapter
- 권한, 감사로그, 에러코드, 운영 안전장치(timeout/watchdog/retry)

## 3. 구현 원칙
1. 계약 우선: `docs/05-api-contract.md` 기준으로 구현하고, 변경은 문서 선반영 후 FE/BE 동시 리뷰.
2. 상태 표준 준수: `docs/06-job-lifecycle.md`의 상태(`queued/running/success/failed/partial_failed`)만 사용.
3. 어댑터 표준화: `docs/07-provider-adapter-spec.md` 인터페이스 고정, provider 특이점은 adapter 내부 캡슐화.
4. 운영 가능성 내장: 감사로그/에러코드/타임아웃/재시도 정책을 1차 구현에서 포함.

## 4. Sprint별 실행 계획

## Sprint 1 (기반)
### 목표
- API와 Job 파이프라인의 최소 동작을 end-to-end로 연결한다.

### 작업 항목
1. DB 스키마 생성
- `skills`
- `providers`
- `install_runs`
- `chat_actions`
- 인덱스: run 상태 조회, 최근 실행 조회, skill/provider 조합 조회

2. API 1차 구현
- `GET /api/skills`
- `POST /api/skills`
- `POST /api/install-runs` (worker mock 기반)
- `GET /api/install-runs/:id`

3. Worker mock 구현
- run 상태 전이 시뮬레이션 (`queued -> running -> success/failed`)
- 상태 변경 시각/사유 저장

4. 기본 운영/보안
- 요청 검증(scheme validation)
- 공통 에러코드 포맷 적용
- 최소 감사로그(생성/실패 이벤트)

### 완료 기준
- Skill 등록 후 목록 반영
- 설치 실행 요청 시 상태 전이 확인 가능
- FE가 polling으로 상태 반영 가능

## Sprint 2 (실행)
### 목표
- 실제 provider 연동과 실패 복구 경로를 완성한다.

### 작업 항목
1. OpenAI adapter 구현
- adapter 인터페이스 구현
- provider 에러 -> 표준 에러코드 매핑

2. 실행 안정성
- retry 정책(횟수/간격/대상 에러)
- rollback 액션 설계 및 구현
- timeout 정책 적용

3. 감사/추적 강화
- 감사로그 상세화(actor/action/target/result)
- run 이벤트 히스토리 저장
- 장애 분석을 위한 상관관계 ID(correlation id) 도입

4. ChatOps 파이프라인 연결
- `POST /api/chat-ops` -> run 생성 파이프라인 연결
- 명령 검증 및 권한 체크

### 완료 기준
- 단일 provider 실설치 성공
- 실패 재시도 동작
- 챗봇 명령으로 run 생성 가능

## Sprint 3 (확장)
### 목표
- 멀티 provider와 부분 실패 처리의 운영 완성도를 높인다.

### 작업 항목
1. Claude/Gemini adapter 추가
- 공통 인터페이스 준수
- provider별 제한/오류 매핑 보강

2. 부분 실패 집계
- `partial_failed` 상태 계산 로직
- 실패 유형별 집계 및 응답 필드 추가

3. 알림/운영 규칙
- watchdog 기반 고착 run 감지
- 알림 규칙(반복 실패, 장시간 실행) 정의 및 연결

### 완료 기준
- 멀티 provider 일괄 설치 성공
- `partial_failed` 상태가 API/대시보드에 일관 반영

## 5. API/데이터 핸드오프 규칙
1. FE 요청 필드는 이슈로 명시하고 우선순위 합의.
2. BE는 구현 전 JSON fixture를 우선 제공.
3. 계약 변경은 문서 -> 리뷰 -> 구현 순서 준수.
4. QA 시나리오는 FE/BE 공동 유지.

## 6. 품질 게이트 (BE)
1. 정적 점검/빌드 통과 (`pnpm lint`, `pnpm build`)
2. 핵심 API 테스트 통과
- skills CRUD(필수 범위)
- install run 생성/조회/상태전이
- chat-ops 명령 처리
3. 실패 경로 테스트 통과
- provider 오류 매핑
- retry/timeout/watchdog 동작

## 7. 리스크 대응 계획
1. Provider API 차이
- 대응: adapter 인터페이스 고정, 표준 에러코드 매핑 테이블 유지

2. FE/BE 일정 불일치
- 대응: fixture 우선 제공, contract test 자동화

3. 장시간 실행 고착
- 대응: timeout + watchdog + 재시도 + 수동 개입(run cancel/retry) 절차

## 8. 즉시 실행 To-do (이번 주)
1. 마이그레이션 초안 작성 및 리뷰
2. `POST /api/install-runs` + mock worker E2E 연결
3. run 상태 조회 API와 이벤트 스키마 확정
4. OpenAI adapter 인터페이스 스켈레톤 작성
5. FE 전달용 fixture 1차 배포
