# Code Rules (Based on nextjs-ai-chatbot)

## 1. 목적과 범위
- 이 문서는 `/Users/2302-n0214/Documents/workspaces6/find-biz` 프로젝트의 기본 구현 규칙이다.
- 기준 템플릿은 `nextjs-ai-chatbot`의 실전 패턴을 따른다.
- 적용 범위: App Router, API Route, DB Query Layer, UI Component, AI Action Layer.

## 2. 기술 기준선
- Next.js App Router + TypeScript `strict: true` 유지.
- 패키지 매니저는 `pnpm` 고정.
- 경로 별칭은 `@/*` 사용.
- 포맷/린트는 Biome + Ultracite 체계를 따른다.

## 3. 폴더/레이어 규칙
- `app/`: 라우트, 레이아웃, 서버 액션, route handler.
- `components/`: 재사용 UI, 화면 조합 컴포넌트.
- `lib/`: 도메인 로직, DB 쿼리, 유틸, 에러 타입.
- `lib/db/`: `schema.ts`, `queries.ts`, `migrations/*`를 단일 진입점으로 유지.
- `hooks/`: 클라이언트 전용 상태/행동 훅.
- `tests/`: e2e 및 핵심 시나리오 테스트.

## 4. TypeScript 규칙
- `any` 사용 금지 원칙. 불가피한 경우 파일 내 주석으로 이유 명시.
- 외부 입력(JSON, FormData, Querystring)은 반드시 `zod` 스키마로 검증.
- API 요청/응답 타입은 `export type`으로 명시하고 route handler와 공유.
- Nullable 데이터는 early return으로 분기하여 중첩을 줄인다.

## 5. API Route 규칙
- `app/**/api/**/route.ts`에서만 HTTP 처리.
- Route는 다음 순서 고정:
1. 입력 파싱/검증(`zod`)
2. 인증/권한 확인
3. 도메인 서비스 호출
4. 응답 직렬화
- 에러는 `lib/errors.ts`의 공통 에러 타입으로 반환한다.
- DB 원인 등 민감 정보는 사용자 응답에 직접 노출하지 않는다.

## 6. 에러 처리 규칙
- 에러 코드는 `type:surface` 형식(`bad_request:api`) 유지.
- 사용자 노출 메시지와 로그 메시지를 분리한다.
- 프론트 fetch 유틸은 비정상 응답을 공통 에러 객체로 변환한다.
- "부분 실패"가 가능한 배치 작업은 `partial_failed` 상태를 반드시 지원한다.

## 7. DB/서버 규칙
- DB 접근 파일에는 `import "server-only";` 적용.
- 쿼리는 반드시 `lib/db/queries.ts` 또는 도메인별 query 파일로 집중화한다.
- Route handler에서 SQL 직접 작성 금지.
- 모든 변경 쿼리는 권한/소유권 조건을 포함한다.
- 마이그레이션 없는 스키마 변경 금지.

## 8. React/Next 구성 규칙
- 기본 원칙: Server Components 우선, Client Components 최소화.
- 클라이언트 컴포넌트에는 `"use client"`를 필요한 파일에만 선언.
- 데이터 패칭 워터폴 방지:
1. 독립 데이터는 `Promise.all`로 병렬화
2. API route에서도 await 지연 패턴 적용(먼저 시작, 나중 await)
- 대형/저빈도 UI는 `next/dynamic`으로 지연 로딩.
- URL 기반 상태(탭, 필터, 정렬)는 search params를 우선 사용.

## 9. 상태 관리 규칙
- 서버 상태는 SWR/서버 패칭으로 관리한다.
- 클라이언트 로컬 UI 상태만 `useState`로 관리한다.
- 동일 데이터에 다중 소스 상태를 만들지 않는다(단일 소스 원칙).

## 10. UI/컴포넌트 규칙
- shadcn/ui primitive를 우선 재사용하고, 도메인 컴포넌트에서 조합한다.
- 컴포넌트는 "표시"와 "행동"을 분리한다.
- 접근성:
1. 버튼/입력에는 명확한 라벨
2. 로딩/실패/빈 상태를 모두 명시
- `data-testid`는 핵심 사용자 흐름 요소에 부여한다.

## 11. AI/작업 실행 규칙 (프로젝트 특화)
- 챗봇 명령은 즉시 부작용 실행 금지, 먼저 Action 파라미터 검증.
- 실행은 동기 처리 대신 Job Queue를 통해 비동기로 처리.
- Job 상태 표준: `queued | running | success | failed | partial_failed`.
- 모든 실행에는 감사 로그(`who`, `when`, `what`, `result`)를 남긴다.

## 12. 보안/환경변수 규칙
- 비밀키는 `.env*`로만 관리하고 코드 하드코딩 금지.
- 환경변수 접근은 앱 시작 시 유효성 검증한다(zod 권장).
- 외부 Provider 토큰은 최소 권한 원칙으로 발급한다.

## 13. 테스트 규칙
- 최소 테스트 단위:
1. 핵심 API 200/4xx/5xx
2. 권한 경계(본인/타인/관리자)
3. 배치 실행 성공/부분실패/재시도
- e2e는 "핵심 사용자 가치 흐름" 기준으로 작성:
1. Skill 등록
2. 설치 실행
3. 상태 확인
4. 실패 재시도

## 14. 네이밍/코드 스타일
- 파일명은 kebab-case, React 컴포넌트는 PascalCase.
- boolean 변수는 `is/has/can` 접두어 사용.
- 함수는 동사형(`getSkills`, `retryFailedRuns`).
- 주석은 "왜"가 필요한 경우에만 짧게 남긴다.

## 15. PR/완료 기준
- `pnpm lint`, `pnpm build`, 관련 테스트 통과가 기본.
- 신규 API는 스키마 검증 + 에러 코드 + 테스트가 함께 있어야 한다.
- 성능 리스크(워터폴, 과도한 클라 상태, 불필요한 번들 증가) 없는지 확인한다.

## 16. 금지 목록
- Route handler에서 검증 없는 `request.json()` 직접 신뢰.
- 인증/권한 확인 없는 데이터 수정.
- UI에서 Provider 비밀값 직접 노출.
- 임시 콘솔 로그를 프로덕션 코드에 방치.
- 대규모 리팩터링을 한 PR에 혼합(기능/구조/스타일 변경 분리).

