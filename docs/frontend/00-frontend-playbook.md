# Frontend Playbook (Canonical)

## 1. 목표
- `/dashboard`, `/skills` 중심 운영 UI를 구현한다.
- 상태머신(`queued/running/success/failed/partial_failed`)을 일관된 UX로 제공한다.
- ChatOps 패널을 통해 같은 실행 파이프라인을 사용한다.

## 2. 구현 원칙
1. 기준 문서:
  - `docs/00-code-rules.md`
  - `docs/05-api-contract.md`
  - `docs/06-job-lifecycle.md`
  - `docs/10-orchestration-plan.md`
2. API 계약 우선, 계약 변경 시 문서 선반영
3. loading/error/empty 상태를 모든 화면/액션에 기본 제공
4. fixture + 실제 API 병행 개발 후 API 우선 모드로 전환

## 3. 화면 범위
1. `/dashboard`
- KPI 카드, 최근 run 테이블, 빠른 액션
2. `/skills`
- skill 목록/검색/필터/등록
- 설치/재시도/롤백 액션
3. 우측 ChatOps 패널
- 자연어 명령 입력, 실행 가능/불가 분기, runIds 연결

## 4. API 연동 체크리스트
- [ ] `/api/skills`: 목록/등록/필터 응답 확인
- [ ] `/api/install-runs`: 실행 생성, 상세 조회, 상태 전이 확인
- [ ] `/api/chat-ops`: accepted true/false 분기 확인
- [ ] 에러 포맷 `{code,message,cause?}` 전 경로 일치 확인

## 5. Sprint 실행 계획
1. Sprint 1 (기반)
- layout/공통 컴포넌트/상태 배지
- skills/dashboard 기본 연동
- run polling 훅

2. Sprint 2 (실행)
- 설치/재시도/롤백 인터랙션
- 실패 상세/재시도 UX
- ChatOps 기본 명령 연동

3. Sprint 3 (확장)
- provider별 상태 시각화 강화
- partial_failed 전용 UX
- 대시보드 필터/알림 고도화

## 6. FE -> BE 핸드오프 핵심
1. install-runs 상태 자동 전이(mock worker 포함)
2. run 상세 조회 계약(`GET /api/install-runs/{id}` 또는 동등 규약)
3. 공통 에러 포맷 일관성
4. provider 상태/오류 필드 계약 고정
5. fixture 제공(success/failed/partial_failed/chatops-rejected)

## 7. QA / Release 게이트
- [ ] 핵심 E2E: Skill 등록, 설치 실행, 실패 재시도, 상태 확인
- [ ] 회귀: 중복 클릭 방지, 폴링 안정성, 네트워크 오류 복구
- [ ] `pnpm lint`, `pnpm build` 통과

## 8. 티켓 우선순위 (요약)
- P0: 상태 전이, run 상세 조회, 에러 포맷 통일
- P1: ChatOps 계약 고정, Providers 계약/fixture
- P2: 멱등 정책, 페이징/정렬 규약

