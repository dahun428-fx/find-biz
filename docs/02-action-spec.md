# Action Spec (Dashboard / Skill)

## 공통 규칙
- 모든 실행 액션은 비동기 Job으로 처리한다.
- 각 Job은 `queued -> running -> success|failed|partial_failed` 상태를 가진다.
- UI는 낙관적 업데이트 대신 서버 상태를 폴링/스트리밍으로 반영한다.

## Dashboard 액션 명세

### 1) 실패 작업 다시 시도
- 위치: Dashboard 빠른 조치
- 입력: 최근 실패 Job 범위(기본 최근 24시간)
- 처리:
  1. 실패 대상 추출
  2. 대상별 재시도 Job 생성
  3. 진행 상태를 실행 현황 테이블에 즉시 반영
- 결과:
  - 성공: 재시도 생성 수, 성공 수, 실패 수 표시
  - 실패: 공통 오류코드 + 개별 대상 오류 링크

### 2) 전체 동기화 실행
- 위치: Dashboard 빠른 조치
- 입력: 없음(MVP 기준 전체 Skill)
- 처리:
  1. 전체 Skill 최신 버전 조회
  2. 설치 대상 Provider별 배포 Job 생성
- 결과:
  - 실행 요약(대기/진행/완료/실패)

### 3) 챗봇 열기
- 위치: 글로벌 헤더/우측 패널
- 목적: 자연어 운영 명령 실행
- 예시 명령:
  - "실패한 설치만 다시 시도해줘"
  - "지난 24시간 실패 원인 Top3 보여줘"

## Skill 액션 명세

### 1) 새 Skill 등록
- 입력: GitHub URL, 선택 옵션(브랜치/태그)
- 처리:
  1. URL 검증
  2. `SKILL.md` 파싱
  3. 메타데이터 저장
- 결과:
  - 성공: 목록 즉시 반영
  - 실패: 파싱 실패 원인/권한 오류 표시

### 2) 단일 설치
- 입력: 선택 Skill + 대상 Provider 1개
- 처리: 설치 Job 1개 생성
- 결과: Provider 상태 갱신

### 3) 다중 Provider 설치
- 입력: 선택 Skill + 대상 Provider N개
- 처리: Provider별 하위 Job 생성(병렬)
- 결과: 전체 성공/부분 실패 요약

### 4) 실패 대상만 재시도
- 입력: 선택 Skill + 최근 실행 범위
- 처리: 실패 하위 Job만 재생성
- 결과: 재시도 결과 누적 표시

### 5) 특정 버전 롤백
- 입력: Skill 버전(ref)
- 처리: 해당 ref 기준 재설치 Job 생성
- 결과: 현재 운영 버전 포인터 갱신

## 챗봇 명령 -> 액션 매핑 (MVP)
- "Skill A를 전체에 설치" -> `bulkInstall(skillId, allProviders)`
- "실패한 것만 재시도" -> `retryFailed(scope)`
- "Skill A 상태 보여줘" -> `getSkillStatus(skillId)`
- "A를 v1.2.0으로 롤백" -> `rollback(skillId, ref)`

## 에러/권한 처리
- 권한 없음: 액션 버튼 비활성 + 이유 툴팁
- 부분 실패: 성공/실패 분리 집계 필수
- 재시도 한도: 동일 대상 최대 N회(기본 3회)

