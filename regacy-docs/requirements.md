# AI Skills Factory - 요구사항 명세서

## 프로젝트 개요

### 목적
AI SKILLS를 보관하고 CRUD가 가능한 형태의 게시판 프로젝트

### 핵심 개념
- **AI SKILLS**: Anthropic에서 제안한 SKILLS 형태
  - 구조: `SKILL.md` (YAML frontmatter + 설명) + `scripts/` + `examples/` + `resources/`
  - GitHub 저장소에서 관리되는 재사용 가능한 AI 도구/워크플로우

### 기술 스택
- **Frontend**: Next.js 15 (App Router) + TypeScript
- **UI Framework**: shadcn/ui + Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **AI**: Google Gemini 2.5 Flash
- **External API**: GitHub API
- **Deployment**: Vercel

---

## 주요 기능 (MVP)

### 1. 사용자 인증 및 역할 관리

#### 인증
- 이메일/비밀번호 기반 회원가입/로그인
- Supabase Auth 사용
- 다중 사용자 지원
- 프로필 페이지 없음 (간소화)

#### 사용자 역할 (Role)
**2단계 역할 시스템:**
- **User (일반 사용자)**: 기본 역할, 회원가입 시 자동 부여
  - SKILL CRUD 가능 (본인 것만)
  - 공유, 즐겨찾기, 복사 가능
  - 제한 사항 없음
  
- **Admin (관리자)**: 시스템 관리자
  - 모든 User 권한 포함
  - 모든 SKILL 수정/삭제 가능
  - 사용자 관리 (역할 변경, 계정 관리)
  - 통계 및 모니터링 대시보드 접근

#### 역할 부여 방식
- 회원가입 시 자동으로 User 역할 부여
- Admin 역할은 기존 관리자가 수동으로 부여
- 최초 관리자는 데이터베이스에서 직접 설정

### 2. SKILL 등록 (GitHub URL + AI 추천)

#### 등록 프로세스
```
Step 1: GitHub URL 입력
  - 사용자가 GitHub 저장소 URL 입력
  - 예: https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design/skills/frontend-design

Step 2: 자동 검증 및 분석 (로딩 상태)
  - GitHub API로 SKILL.md 파일 가져오기
  - YAML frontmatter 파싱 (name, description 추출)
  - Gemini AI로 카테고리/태그 분석 및 추천
  - 실패 시: 사용자에게 "재시도" 버튼 제공 또는 수동 입력 모드

Step 3: 등록 폼 (AI 추천 포함)
  [자동 입력] Title: ___
  [자동 입력] Description: ___
  [AI 추천 🤖] 카테고리: ___ (수정 가능, '>' 구분자로 계층 표현)
  [AI 추천 🤖] 태그: ___, ___, ___ (추가/삭제 가능)
  [선택 입력] 개인 메모: ___
  [버튼] 등록 | 취소
```

#### AI 추천 로직
- 사용자의 기존 카테고리/태그 목록 확인
- SKILL 내용 분석 (title, description 기반)
- 적합한 카테고리 계층 구조 추천 (최대 5depth)
- 관련 태그 추천
- 사용자는 AI 추천을 수락/수정/거부 가능

#### 카테고리 시스템
- **계층 구조**: 최대 5depth
- **입력 형식**: `개발>프론트엔드>React>Hooks>최적화`
- **저장 형식**: PostgreSQL JSONB 배열 `["개발", "프론트엔드", "React", "Hooks", "최적화"]`
- **자유 생성**: 사용자가 새 카테고리를 자유롭게 생성 가능
- **AI 추천**: 기존 카테고리 우선 추천, 필요 시 새 카테고리 제안

#### 태그 시스템
- **입력 형식**: `#` 기호로 시작하는 자유 입력 (예: `#react`, `#typescript`, `#hooks`)
- **저장 형식**: PostgreSQL JSONB 배열 `["react", "typescript", "hooks"]` (# 제외하고 저장)
- **검색 기능**: 태그로 SKILL 검색 가능
- **태그 클릭**: 카드나 상세 페이지에서 태그 클릭 시 해당 태그로 필터링
- **AI 추천**: SKILL 내용 분석 후 관련 태그 추천 (사용자가 수정/추가/삭제 가능)

### 3. SKILL 목록 보기

#### 탭 구조 (3개)
1. **전체 SKILLS**: 모든 사용자가 등록한 SKILLS
2. **내 SKILLS**: 현재 사용자가 등록한 SKILLS
3. **공유받은 SKILLS**: 다른 사용자가 나에게 공유한 SKILLS

#### 레이아웃
```
┌─────────────────────────────────────────────────────────┐
│ [로고] [전체 SKILLS] [내 SKILLS] [공유받은]  [@username] │
├──────────┬──────────────────────────────────────────────┤
│ [☰]      │ [🔍 검색...] [정렬: 최신순 ▼] [+ 새 SKILL]   │
│          │                                               │
│ 카테고리  │ ┌──────┐ ┌──────┐ ┌──────┐                  │
│          │ │SKILL │ │SKILL │ │SKILL │                  │
│ > 개발   │ │  1   │ │  2   │ │  3   │                  │
│   > 프론트│ │ ⭐ 5 │ │ ⭐ 3 │ │ ⭐ 8 │                  │
│     > UI │ └──────┘ └──────┘ └──────┘                  │
│   > 백엔드│ ┌──────┐ ┌──────┐ ┌──────┐                  │
│ > 디자인  │ │SKILL │ │SKILL │ │SKILL │                  │
│          │ │  4   │ │  5   │ │  6   │                  │
│          │ └──────┘ └──────┘ └──────┘                  │
└──────────┴──────────────────────────────────────────────┘
```

#### 사이드바 (카테고리 트리)
- 접기/펼치기 가능 (모바일 대응)
- 계층 구조 표시
- 카테고리 클릭 시 하위 카테고리 포함 필터링
- 여러 카테고리 동시 선택: Phase 2 (고도화)

#### SKILL 카드
**카드에 표시:**
- SKILL 이름
- 설명 (요약, 2-3줄)
- 카테고리 (최상위 또는 전체 경로)
- 즐겨찾기 버튼 + 즐겨찾기 수

**상세 페이지에만 표시:**
- 작성자
- 등록일
- 전체 태그 목록
- GitHub URL (바로가기 링크)
- 개인 메모
- 전체 설명
- 복사/공유 버튼

### 4. 검색 및 필터링

#### 검색
- **위치**: 정렬 버튼 왼쪽
- **동작**: 실시간 검색 (타이핑 시 즉시 필터링)
- **범위**: 현재 활성화된 탭 내에서만 검색
  - 전체 SKILLS 탭: 모든 SKILLS 검색
  - 내 SKILLS 탭: 내 SKILLS만 검색
  - 공유받은 탭: 공유받은 SKILLS만 검색
- **검색 대상**: 이름, description, 카테고리, 태그

#### 정렬 옵션
- 최신순 (created_at DESC)
- 오래된순 (created_at ASC)
- 이름순 (title ASC)
- 즐겨찾기순 (favorites count DESC)
- 복합 정렬: Phase 2 (고도화)

### 5. 즐겨찾기
- 모든 SKILLS에 즐겨찾기 가능 (전체/내/공유받은 모두)
- 카드에 즐겨찾기 버튼 표시
- 즐겨찾기 수 표시
- 사용자별로 독립적으로 관리

### 6. 복사 기능 (Fork 대신)
- 다른 사용자의 SKILL을 내 SKILL로 복사
- 복사 후 완전히 독립적으로 관리
- 원본 추적 없음 (단순 복사)
- 복사 후 자유롭게 수정 가능

### 7. 공유 기능
- **공유 방법**: 이메일 주소 입력
- **동작**: 
  - 내 SKILL을 다른 사용자에게 공유
  - 받은 사람의 "공유받은 SKILLS" 탭에 표시
  - 같은 SKILL을 같은 사람에게 여러 번 공유 가능 (중복 허용)
  - 공유받은 SKILL은 받은 사람의 고유 SKILL이 됨 (독립적으로 관리)
  - 공유받은 SKILL도 즐겨찾기, 수정, 삭제 가능
  - 원본 SKILL이 삭제되어도 공유받은 SKILL은 유지됨
- **공유 취소**: Phase 1에서는 지원하지 않음
- **알림**: 없음 (Phase 1에서는 제외)

### 8. SKILL 수정/삭제
- 본인이 등록한 SKILL만 수정/삭제 가능
- 공유받은 SKILL도 수정/삭제 가능 (독립적으로 관리)
- 수정: 모든 필드 수정 가능 (GitHub URL 제외 권장)
- 삭제: 하드 삭제 (완전 제거)

### 9. 페이지네이션
- **방식**: 숫자 페이지네이션 (1, 2, 3, 4, 5...)
- **페이지당 항목 수**: 12개 (3열 × 4행 기준)
- **UI**: 이전/다음 버튼 + 페이지 번호 버튼
- **무한 스크롤**: 사용하지 않음

### 10. 관리자 기능

#### 관리자 대시보드 (`/admin`)
**접근 권한**: Admin 역할만 접근 가능

**사용자 관리**:
- 전체 사용자 목록 조회
- 사용자 검색 (이메일, 이름)
- 사용자 역할 변경 (User ↔ Admin)
- 사용자 계정 정지/활성화
- 사용자 계정 삭제

**SKILL 관리**:
- 모든 SKILL 목록 조회
- 모든 SKILL 수정 권한
- 모든 SKILL 삭제 권한
- SKILL 검색 및 필터링

**통계 및 모니터링**:
- 전체 통계
  - 총 사용자 수
  - 총 SKILL 수
  - 총 즐겨찾기 수
  - 총 공유 수
- 최근 활동
  - 최근 가입한 사용자 (10명)
  - 최근 등록된 SKILL (10개)
- 인기 SKILL
  - 즐겨찾기 많은 순 (Top 10)
  - 최근 7일 인기 SKILL

### 11. 에러 처리
- **GitHub URL 오류**:
  - 404 Not Found: "GitHub 저장소를 찾을 수 없습니다. URL을 확인해주세요."
  - SKILL.md 없음: "SKILL.md 파일을 찾을 수 없습니다. 올바른 SKILL 경로인지 확인해주세요."
  - YAML frontmatter 오류: "SKILL.md의 형식이 올바르지 않습니다. name과 description을 확인해주세요."
- **AI 추천 오류**:
  - API 할당량 초과: "AI 추천 서비스가 일시적으로 사용 불가합니다. 수동으로 입력해주세요."
  - 네트워크 오류: "AI 추천을 가져오는 중 오류가 발생했습니다. 재시도 버튼을 눌러주세요."
- **권한 오류**:
  - 수정/삭제 권한 없음: "본인이 등록한 SKILL만 수정/삭제할 수 있습니다."
  - 로그인 필요: "이 기능을 사용하려면 로그인이 필요합니다."
- **공유 오류**:
  - 존재하지 않는 이메일: "해당 이메일로 가입된 사용자가 없습니다."
  - 본인에게 공유: "자신에게는 SKILL을 공유할 수 없습니다."

---

## 데이터베이스 스키마

### users
```sql
- id: UUID (PK)
- email: VARCHAR (UNIQUE)
- password_hash: VARCHAR
- role: VARCHAR (기본값: 'user', 'user' | 'admin')
- is_active: BOOLEAN (기본값: true)
- created_at: TIMESTAMP
```

### skills
```sql
- id: UUID (PK)
- user_id: UUID (FK -> users.id)
- title: VARCHAR
- description: TEXT
- github_url: VARCHAR
- category_path: JSONB (예: ["개발", "프론트엔드", "React"])
- tags: JSONB (예: ["react", "hooks", "optimization"])
- memo: TEXT (개인 메모, nullable)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### favorites
```sql
- id: UUID (PK)
- user_id: UUID (FK -> users.id)
- skill_id: UUID (FK -> skills.id)
- created_at: TIMESTAMP
- UNIQUE(user_id, skill_id)
```

### shared_skills
```sql
- id: UUID (PK)
- skill_id: UUID (FK -> skills.id)
- from_user_id: UUID (FK -> users.id)
- to_user_email: VARCHAR
- created_at: TIMESTAMP
```

---

## Phase 2 (고도화 기능)

### 추후 개발 예정
1. **MCP 형태 파일 열람**
   - SKILL 상세 페이지에서 GitHub 파일 트리 탐색
   - 파일 내용 직접 보기 (코드 하이라이팅)

2. **소셜 로그인**
   - Google, GitHub OAuth

3. **복합 필터링/정렬**
   - 여러 조건 동시 적용
   - 고급 검색 옵션

4. **여러 카테고리 동시 선택**
   - 멀티 셀렉트 필터

5. **GitHub 자동 동기화**
   - 저장소 업데이트 시 SKILL 자동 갱신
   - Webhook 연동

6. **공유 알림**
   - 이메일 알림
   - 인앱 알림

7. **버전 관리**
   - SKILL 수정 이력 추적
   - 이전 버전 복원

8. **GraphDB 관계 시각화**
   - SKILL 간 관계 표현
   - 의존성 그래프

---

## 기술 상세

### Gemini API 설정
- **모델**: gemini-2.5-flash
- **API 키**: 개발자가 환경변수로 관리 (`.env.local`)
- **용도**: 
  - SKILL 등록 시 카테고리/태그 자동 추천
  - SKILL 내용 분석
- **에러 처리**: 
  - API 할당량 초과 시 사용자에게 수동 입력 안내
  - 네트워크 오류 시 재시도 옵션 제공

### GitHub API
- **용도**: 
  - SKILL.md 파일 내용 가져오기
  - YAML frontmatter 파싱
- **제약**: Public 저장소만 지원 (Phase 1)

### Supabase
- **Database**: PostgreSQL
- **Auth**: 이메일/비밀번호 인증
- **Storage**: 사용 안 함 (GitHub URL만 저장)

---

## UI/UX 원칙

### 디자인 가이드
- **스타일**: 모던하고 깔끔한 디자인
- **컬러**: shadcn/ui 기본 테마 활용
- **반응형**: 모바일/태블릿/데스크톱 대응
- **접근성**: WCAG 2.1 AA 준수

### 사용자 편의성
- **빠른 등록**: GitHub URL만으로 간편 등록
- **AI 추천**: 카테고리/태그 자동 제안으로 입력 최소화
- **실시간 검색**: 즉각적인 피드백
- **직관적 네비게이션**: 명확한 탭 구조

---

## 개발 우선순위

### Phase 1 (MVP) - 4주
1. 프로젝트 초기 설정 (Next.js + Supabase)
2. 인증 시스템 (회원가입/로그인)
3. SKILL CRUD (등록/수정/삭제)
4. GitHub API + Gemini AI 연동
5. 3개 탭 UI 구현
6. 검색/필터링/정렬
7. 즐겨찾기 기능
8. 복사/공유 기능

### Phase 2 (고도화) - TBD
- 위 "Phase 2 (고도화 기능)" 섹션 참조

---

## 성공 기준

### MVP 완료 조건
- [ ] 사용자가 이메일로 가입하고 로그인할 수 있다
- [ ] GitHub URL을 입력하면 AI가 카테고리/태그를 추천한다
- [ ] SKILL을 등록/수정/삭제할 수 있다
- [ ] 전체/내/공유받은 SKILLS를 탭으로 구분해서 볼 수 있다
- [ ] 실시간 검색으로 SKILL을 찾을 수 있다
- [ ] 카테고리로 필터링할 수 있다
- [ ] 정렬 옵션으로 목록을 정렬할 수 있다
- [ ] SKILL을 즐겨찾기할 수 있다
- [ ] 다른 사용자의 SKILL을 복사할 수 있다
- [ ] 이메일로 SKILL을 공유할 수 있다

---

## 참고 자료

- Anthropic SKILLS 예시: https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design/skills
- Next.js 문서: https://nextjs.org/docs
- Supabase 문서: https://supabase.com/docs
- shadcn/ui: https://ui.shadcn.com
- Gemini API: https://ai.google.dev/gemini-api/docs
