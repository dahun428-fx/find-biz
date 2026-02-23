# Archive Policy

이 폴더는 **참조용 보관 문서**를 저장합니다.  
아카이브 문서는 구현 기준(Source of Truth)이 아닙니다.

## 보관 기준
1. 현재 문서(`docs/`)와 내용이 중복되는 문서
2. 이전 제품 방향(레거시 요구사항) 문서
3. 과거 핸드오프 결과물로 유지가 필요한 문서

## 현재 보관된 세트
- `docs/archive/regacy-docs/`
  - 초기 AI Skills Factory 보드형 기획 문서 요약본(`SUMMARY.md`)
- `docs/archive/backend-docs/`
  - `docs/backend/*`로 통합되기 전 백엔드 실행 문서 요약본(`SUMMARY.md`)
- `docs/archive/frontend-docs/`
  - `docs/frontend/*` 분산 문서를 통합하기 전 프론트 실행 문서 요약본(`SUMMARY.md`)

## 사용 규칙
1. 아카이브 문서는 "참고"로만 사용하고, 구현 계약은 `docs/` 기준으로 판단한다.
2. 아카이브 내용이 필요하면 `docs/`의 canonical 문서로 재반영 후 사용한다.
3. 2차 정리 이후 아카이브는 원문 묶음 대신 요약본만 유지한다.
