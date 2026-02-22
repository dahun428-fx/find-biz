# AI Skills Factory - 개발 계획

## Phase 1: MVP 개발 (4주)

### Week 1: 프로젝트 초기 설정 및 인증

- [ ] **프로젝트 초기화**
  - [ ] Next.js 15 프로젝트 생성 (App Router, TypeScript)
  - [ ] shadcn/ui + Tailwind CSS 설정
  - [ ] 프로젝트 구조 설계 및 폴더 구성
  - [ ] ESLint, Prettier 설정
  - [ ] Git 저장소 초기화

- [ ] **Supabase 설정**
  - [ ] Supabase 프로젝트 생성
  - [ ] 데이터베이스 스키마 마이그레이션
    - [ ] users 테이블
    - [ ] skills 테이블
    - [ ] favorites 테이블
    - [ ] shared_skills 테이블
  - [ ] RLS 정책 적용
  - [ ] Supabase 클라이언트 설정

- [ ] **인증 시스템**
  - [ ] Supabase Auth 설정
  - [ ] 회원가입 페이지 (`/signup`)
  - [ ] 로그인 페이지 (`/login`)
  - [ ] 로그아웃 기능
  - [ ] 인증 미들웨어 (보호된 라우트)
  - [ ] 사용자 세션 관리

---

### Week 2: SKILL CRUD 및 AI 연동

- [ ] **GitHub API 연동**
  - [ ] GitHub API 클라이언트 설정
  - [ ] SKILL.md 파일 가져오기 함수
  - [ ] YAML frontmatter 파싱 (gray-matter 라이브러리)
  - [ ] GitHub URL 검증 로직

- [ ] **Gemini AI 연동**
  - [ ] Gemini API 클라이언트 설정 (환경변수)
  - [ ] 카테고리 추천 프롬프트 작성
  - [ ] 태그 추천 프롬프트 작성
  - [ ] AI 응답 파싱 및 에러 핸들링

- [ ] **SKILL 등록 기능**
  - [ ] SKILL 등록 페이지 (`/skills/new`)
  - [ ] Step 1: GitHub URL 입력 폼
  - [ ] Step 2: 로딩 상태 (GitHub API + AI 분석)
  - [ ] Step 3: 등록 폼 (AI 추천 포함)
    - [ ] Title (자동 입력)
    - [ ] Description (자동 입력)
    - [ ] 카테고리 입력 (AI 추천, 수정 가능)
    - [ ] 태그 입력 (AI 추천, 추가/삭제)
    - [ ] 개인 메모 (선택)
  - [ ] AI 재시도 버튼
  - [ ] 등록 API 엔드포인트 (`POST /api/skills`)

- [ ] **SKILL 수정/삭제**
  - [ ] SKILL 수정 페이지 (`/skills/[id]/edit`)
  - [ ] 수정 API 엔드포인트 (`PATCH /api/skills/[id]`)
  - [ ] 삭제 API 엔드포인트 (`DELETE /api/skills/[id]`)
  - [ ] 권한 검증 (본인만 수정/삭제)

---

### Week 3: UI 구현 (목록, 검색, 필터링)

- [ ] **메인 레이아웃**
  - [ ] 헤더 컴포넌트
    - [ ] 로고
    - [ ] 탭 네비게이션 (전체/내/공유받은)
    - [ ] 사용자 메뉴 (로그아웃)
  - [ ] 사이드바 컴포넌트
    - [ ] 카테고리 트리 구조
    - [ ] 접기/펼치기 기능
    - [ ] 카테고리 클릭 필터링
  - [ ] 반응형 레이아웃 (모바일 대응)

- [ ] **SKILL 목록 페이지**
  - [ ] 전체 SKILLS 탭 (`/`)
  - [ ] 내 SKILLS 탭 (`/my-skills`)
  - [ ] 공유받은 SKILLS 탭 (`/shared`)
  - [ ] SKILL 카드 컴포넌트
    - [ ] 이름, 설명, 카테고리 표시
    - [ ] 즐겨찾기 버튼 + 개수
  - [ ] 카드 그리드 레이아웃 (3-4열)

- [ ] **검색 및 정렬**
  - [ ] 검색바 컴포넌트 (실시간 검색)
  - [ ] 정렬 드롭다운
    - [ ] 최신순
    - [ ] 오래된순
    - [ ] 이름순
    - [ ] 즐겨찾기순
  - [ ] 검색 API (`GET /api/skills/search`)
  - [ ] 탭별 독립 검색 로직

- [ ] **카테고리 필터링**
  - [ ] 카테고리 목록 생성 (모든 SKILLS에서 추출)
  - [ ] 계층 구조 파싱 (`"['개발', '프론트엔드']"` → 트리)
  - [ ] 하위 카테고리 포함 필터링
  - [ ] 필터 API (`GET /api/skills?category=...`)

---

### Week 4: 즐겨찾기, 복사, 공유 및 상세 페이지

- [ ] **즐겨찾기 기능**
  - [ ] 즐겨찾기 추가/제거 API (`POST/DELETE /api/favorites`)
  - [ ] 즐겨찾기 버튼 UI (하트 아이콘)
  - [ ] 즐겨찾기 수 실시간 업데이트
  - [ ] 즐겨찾기순 정렬 구현

- [ ] **복사 기능**
  - [ ] 복사 API (`POST /api/skills/[id]/copy`)
  - [ ] 복사 버튼 UI (상세 페이지)
  - [ ] 복사 성공 시 "내 SKILLS"로 리다이렉트

- [ ] **공유 기능**
  - [ ] 공유 모달 컴포넌트
  - [ ] 이메일 입력 폼
  - [ ] 공유 API (`POST /api/skills/[id]/share`)
  - [ ] 이메일 검증 (users 테이블 확인)
  - [ ] 공유받은 SKILLS 목록 구현

- [ ] **SKILL 상세 페이지**
  - [ ] 상세 페이지 레이아웃 (`/skills/[id]`)
  - [ ] 전체 정보 표시
    - [ ] 제목, 설명
    - [ ] 작성자, 등록일
    - [ ] 카테고리, 태그
    - [ ] GitHub URL (링크)
    - [ ] 개인 메모 (본인만)
  - [ ] 액션 버튼
    - [ ] 즐겨찾기
    - [ ] 복사
    - [ ] 공유
    - [ ] 수정/삭제 (본인만)

- [ ] **최종 테스트 및 배포**
  - [ ] 전체 기능 통합 테스트
  - [ ] 버그 수정
  - [ ] Vercel 배포 설정
  - [ ] 환경변수 설정 (Gemini API 키)
  - [ ] 프로덕션 배포

---

## Phase 2: 고도화 기능 (TBD)

### 추후 개발 예정

- [ ] **MCP 형태 파일 열람**
  - [ ] GitHub 파일 트리 API 연동
  - [ ] 파일 탐색기 UI
  - [ ] 코드 하이라이팅 (Prism.js 또는 Shiki)
  - [ ] 마크다운 렌더링

- [ ] **소셜 로그인**
  - [ ] Google OAuth 연동
  - [ ] GitHub OAuth 연동
  - [ ] Supabase Auth Provider 설정

- [ ] **복합 필터링/정렬**
  - [ ] 여러 조건 동시 적용 UI
  - [ ] 고급 검색 옵션
  - [ ] 필터 저장 기능

- [ ] **여러 카테고리 동시 선택**
  - [ ] 멀티 셀렉트 UI
  - [ ] OR 조건 필터링

- [ ] **GitHub 자동 동기화**
  - [ ] GitHub Webhook 설정
  - [ ] 저장소 업데이트 감지
  - [ ] SKILL 자동 갱신 로직

- [ ] **공유 알림**
  - [ ] 이메일 알림 (SendGrid 또는 Resend)
  - [ ] 인앱 알림 시스템
  - [ ] notifications 테이블 추가

- [ ] **버전 관리**
  - [ ] skill_versions 테이블 추가
  - [ ] 수정 이력 추적
  - [ ] 이전 버전 복원 기능

- [ ] **GraphDB 관계 시각화**
  - [ ] Neo4j 연동 검토
  - [ ] SKILL 간 관계 정의
  - [ ] 관계 그래프 UI (D3.js 또는 Cytoscape.js)

---

## 개발 가이드라인

### 코드 스타일
- TypeScript strict mode 사용
- ESLint + Prettier 자동 포맷팅
- 컴포넌트는 함수형으로 작성
- 재사용 가능한 컴포넌트는 `/components` 폴더에 분리

### API 설계
- RESTful API 원칙 준수
- `/api/skills` - SKILL CRUD
- `/api/favorites` - 즐겨찾기
- `/api/shared-skills` - 공유
- 에러 핸들링: 일관된 에러 응답 형식

### 상태 관리
- Server Components 우선 사용
- Client Components는 필요한 경우만
- React Query (TanStack Query) 고려 (데이터 캐싱)

### 보안
- Supabase RLS 활용
- API 엔드포인트 권한 검증
- XSS, CSRF 방어
- 환경변수로 민감 정보 관리

### 성능 최적화
- Next.js Image 컴포넌트 사용
- 코드 스플리팅
- 무한 스크롤 또는 페이지네이션 (SKILL 목록)
- 검색 디바운싱 (300ms)

---

## 참고 사항

### 개발 환경
- Node.js 18+
- npm 또는 pnpm
- VS Code (권장)

### 필수 환경변수
```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
GEMINI_API_KEY=
```

### 유용한 라이브러리
- `gray-matter`: YAML frontmatter 파싱
- `@supabase/supabase-js`: Supabase 클라이언트
- `@google/generative-ai`: Gemini API
- `octokit`: GitHub API 클라이언트
- `zod`: 스키마 검증
- `react-hook-form`: 폼 관리
- `sonner`: 토스트 알림
