# 환경 설정 가이드

## 개발 환경 요구사항

### 필수 소프트웨어
- **Node.js**: 18.0.0 이상
- **npm**: 9.0.0 이상 (또는 pnpm 8.0.0 이상)
- **Git**: 최신 버전
- **VS Code**: 권장 (선택사항)

### 계정 준비
- **Supabase 계정**: https://supabase.com
- **Gemini API 키**: https://ai.google.dev
- **GitHub 계정**: (선택사항, Private 저장소 접근 시)

---

## 1단계: 프로젝트 클론 및 초기화

### 1.1 저장소 클론
```bash
git clone https://github.com/your-username/skills-factory.git
cd skills-factory
```

### 1.2 의존성 설치
```bash
npm install
# 또는
pnpm install
```

---

## 2단계: Supabase 설정

### 2.1 Supabase 프로젝트 생성

1. https://supabase.com 접속
2. "New Project" 클릭
3. 프로젝트 정보 입력:
   - **Name**: skills-factory
   - **Database Password**: 안전한 비밀번호 생성 (저장 필수!)
   - **Region**: 가까운 지역 선택 (예: Northeast Asia (Seoul))
4. "Create new project" 클릭

### 2.2 데이터베이스 스키마 생성

1. Supabase 대시보드에서 "SQL Editor" 클릭
2. "New query" 클릭
3. 다음 SQL 실행:

```sql
-- users 테이블 (Supabase Auth가 자동 생성하므로 생략 가능)

-- skills 테이블
CREATE TABLE skills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  github_url VARCHAR(500) NOT NULL,
  category_path JSONB DEFAULT '[]'::jsonb,
  tags JSONB DEFAULT '[]'::jsonb,
  memo TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_skills_user_id ON skills(user_id);
CREATE INDEX idx_skills_created_at ON skills(created_at DESC);
CREATE INDEX idx_skills_title ON skills(title);
CREATE INDEX idx_skills_category_path ON skills USING GIN(category_path);
CREATE INDEX idx_skills_tags ON skills USING GIN(tags);

-- favorites 테이블
CREATE TABLE favorites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, skill_id)
);

CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_skill_id ON favorites(skill_id);
CREATE INDEX idx_favorites_created_at ON favorites(created_at DESC);

-- shared_skills 테이블
CREATE TABLE shared_skills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  from_user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  to_user_email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_shared_skills_to_user_email ON shared_skills(to_user_email);
CREATE INDEX idx_shared_skills_skill_id ON shared_skills(skill_id);
CREATE INDEX idx_shared_skills_from_user_id ON shared_skills(from_user_id);
```

4. "Run" 클릭하여 실행

### 2.3 RLS (Row Level Security) 정책 설정

1. 같은 SQL Editor에서 다음 실행:

```sql
-- skills 테이블 RLS 활성화
ALTER TABLE skills ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 모든 SKILL 읽기 가능
CREATE POLICY "Anyone can view skills"
ON skills FOR SELECT
USING (true);

-- 본인이 등록한 SKILL만 수정 가능
CREATE POLICY "Users can update own skills"
ON skills FOR UPDATE
USING (auth.uid() = user_id);

-- 본인이 등록한 SKILL만 삭제 가능
CREATE POLICY "Users can delete own skills"
ON skills FOR DELETE
USING (auth.uid() = user_id);

-- 인증된 사용자만 SKILL 등록 가능
CREATE POLICY "Authenticated users can insert skills"
ON skills FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- favorites 테이블 RLS
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own favorites"
ON favorites FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own favorites"
ON favorites FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own favorites"
ON favorites FOR DELETE
USING (auth.uid() = user_id);

-- shared_skills 테이블 RLS
ALTER TABLE shared_skills ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view relevant shared skills"
ON shared_skills FOR SELECT
USING (
  auth.uid() = from_user_id 
  OR to_user_email = (SELECT email FROM auth.users WHERE id = auth.uid())
);

CREATE POLICY "Users can share own skills"
ON shared_skills FOR INSERT
WITH CHECK (
  auth.uid() = from_user_id
  AND EXISTS (SELECT 1 FROM skills WHERE id = skill_id AND user_id = auth.uid())
);
```

### 2.4 Supabase 인증 키 확인

1. Supabase 대시보드에서 "Settings" → "API" 클릭
2. 다음 정보 복사:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: `eyJhbGc...`
   - **service_role key**: `eyJhbGc...` (주의: 절대 공개하지 말 것!)

---

## 3단계: Gemini API 키 발급

### 3.1 Google AI Studio 접속
1. https://ai.google.dev 접속
2. "Get API key" 클릭
3. "Create API key" 클릭
4. API 키 복사 (예: `AIzaSyC...`)

---

## 4단계: 환경 변수 설정

### 4.1 `.env.local` 파일 생성

프로젝트 루트에 `.env.local` 파일 생성:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Gemini AI
GEMINI_API_KEY=AIzaSyC...

# GitHub (선택사항, Private 저장소 접근 시)
GITHUB_TOKEN=ghp_...
```

### 4.2 `.env.example` 파일 생성 (Git 커밋용)

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# GitHub (선택사항)
GITHUB_TOKEN=your_github_token
```

### 4.3 `.gitignore` 확인

`.gitignore`에 다음이 포함되어 있는지 확인:

```
.env.local
.env*.local
```

---

## 5단계: 개발 서버 실행

### 5.1 개발 서버 시작
```bash
npm run dev
# 또는
pnpm dev
```

### 5.2 브라우저에서 확인
```
http://localhost:3000
```

---

## 6단계: VS Code 설정 (권장)

### 6.1 권장 확장 프로그램 설치

`.vscode/extensions.json` 파일 생성:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "supabase.supabase-vscode"
  ]
}
```

### 6.2 VS Code 설정

`.vscode/settings.json` 파일 생성:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ]
}
```

---

## 7단계: 데이터베이스 테스트

### 7.1 테스트 데이터 삽입 (선택사항)

Supabase SQL Editor에서 실행:

```sql
-- 테스트용 SKILL 데이터 삽입 (user_id는 실제 사용자 ID로 변경)
INSERT INTO skills (user_id, title, description, github_url, category_path, tags)
VALUES (
  'your-user-uuid',
  'Frontend Design',
  'A comprehensive guide for modern UI/UX design principles and best practices.',
  'https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design/skills/frontend-design',
  '["개발", "프론트엔드", "UI"]'::jsonb,
  '["design", "ui", "frontend"]'::jsonb
);
```

---

## 8단계: 배포 (Vercel)

### 8.1 Vercel 계정 생성
1. https://vercel.com 접속
2. GitHub 계정으로 로그인

### 8.2 프로젝트 배포
1. Vercel 대시보드에서 "New Project" 클릭
2. GitHub 저장소 선택
3. 환경 변수 설정:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `GEMINI_API_KEY`
4. "Deploy" 클릭

### 8.3 배포 확인
```
https://your-project.vercel.app
```

---

## 문제 해결 (Troubleshooting)

### 문제 1: Supabase 연결 오류
**증상**: "Failed to connect to Supabase"

**해결책**:
1. `.env.local` 파일의 Supabase URL과 키 확인
2. Supabase 프로젝트가 활성화되어 있는지 확인
3. 개발 서버 재시작: `npm run dev`

---

### 문제 2: Gemini API 오류
**증상**: "AI 추천을 가져오는 중 오류가 발생했습니다"

**해결책**:
1. Gemini API 키가 올바른지 확인
2. API 할당량 확인: https://ai.google.dev
3. 네트워크 연결 확인

---

### 문제 3: RLS 정책 오류
**증상**: "Row Level Security policy violation"

**해결책**:
1. Supabase SQL Editor에서 RLS 정책 확인
2. 사용자가 로그인되어 있는지 확인
3. `auth.uid()`가 올바르게 설정되어 있는지 확인

---

### 문제 4: 포트 충돌
**증상**: "Port 3000 is already in use"

**해결책**:
```bash
# 다른 포트로 실행
PORT=3001 npm run dev
```

---

## 유용한 명령어

### 개발
```bash
# 개발 서버 시작
npm run dev

# 타입 체크
npm run type-check

# 린트 검사
npm run lint

# 포맷팅
npm run format
```

### 빌드
```bash
# 프로덕션 빌드
npm run build

# 프로덕션 서버 시작
npm start
```

### 데이터베이스
```bash
# Supabase 로컬 개발 환경 시작 (선택사항)
npx supabase start

# 마이그레이션 생성
npx supabase migration new migration_name

# 마이그레이션 적용
npx supabase db push
```

---

## 다음 단계

환경 설정이 완료되었습니다! 이제 다음을 진행할 수 있습니다:

1. **개발 시작**: `docs/todo.md` 참조
2. **API 문서**: `docs/api-spec.md` 참조
3. **UI 디자인**: `docs/ui-design.md` 참조
4. **데이터베이스**: `docs/schema.md` 참조

---

## 추가 리소스

- **Next.js 문서**: https://nextjs.org/docs
- **Supabase 문서**: https://supabase.com/docs
- **shadcn/ui**: https://ui.shadcn.com
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Gemini API**: https://ai.google.dev/gemini-api/docs
- **GitHub API**: https://docs.github.com/en/rest
