# Job Lifecycle (Install Runs)

## 목적
- 설치/동기화/재시도/롤백 작업의 상태 전이와 실패 복구 규칙을 정의한다.

## 상태 정의
- `queued`: 큐에 등록됨, 아직 실행되지 않음
- `running`: 실행 중
- `success`: 정상 완료
- `failed`: 완전 실패
- `partial_failed`: 배치 하위 작업 일부 실패

## 전이 규칙
1. `queued -> running`
2. `running -> success | failed | partial_failed`
3. `failed -> queued` (retry 시 새 run 생성 권장)
4. `partial_failed -> queued` (실패 대상만 retry)

## 실행 단위
- 권장: provider 단위 run을 기본으로 생성  
  - 장점: 실패 분리가 명확하고 재시도 대상 추출이 쉽다.
- 대안: 배치 run + child run  
  - 확장 시 parent/child 구조 도입

## 재시도 정책 (MVP)
- 최대 재시도 횟수: 3회
- 재시도 간격: 지수 백오프(예: 10s, 30s, 90s)
- 재시도 대상:
  - `failed` 전부
  - `partial_failed`의 실패 하위 대상만

## 타임아웃 규칙 (MVP)
- provider 호출 타임아웃(예: 60초)
- 타임아웃 발생 시 `failed` 처리 + `error_code=timeout`

## 멱등성(Idempotency)
- 동일 액션 중복 실행 방지 키:
  - `skill_id + provider_id + action + requested_ref + request_window`
- 같은 키로 요청되면 기존 `queued/running` run 재사용 또는 거절

## 부분 실패 처리
- UI는 집계와 상세를 동시에 표시:
1. 집계: 성공 N / 실패 M
2. 상세: provider별 오류 코드/메시지
- 챗봇 응답도 동일 포맷으로 제공

## 최소 로그 필드
- `run_id`
- `trigger_source` (`ui|chatbot|system`)
- `input` (action/ref/targets)
- `status transitions`
- `error_code`, `error_message`
- `started_at`, `finished_at`, `duration_ms`

## 운영 알림 트리거 (MVP)
- 동일 provider 연속 실패 3회 이상
- 15분 이상 `running` 상태 지속
- 전체 성공률 임계치 하락(예: < 80%)

