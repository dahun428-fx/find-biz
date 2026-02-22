# 데이터베이스 스키마 설계

## Supabase (PostgreSQL) 스키마

### 1. users 테이블

사용자 계정 정보를 저장합니다.

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) DEFAULT 'user' NOT NULL CHECK (role IN ('user', 'admin')),
  is_active BOOLEAN DEFAULT true NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_users_email ON users(email);
```

**필드 설명:**
- `id`: 사용자 고유 식별자 (UUID)
- `email`: 로그인용 이메일 (중복 불가)
- `password_hash`: 해시된 비밀번호 (bcrypt 사용 권장)
- `role`: 사용자 역할 ('user' 또는 'admin', 기본값: 'user')
- `is_active`: 계정 활성화 상태 (기본값: true)
- `created_at`: 계정 생성 시간

---

### 2. skills 테이블

AI SKILL 정보를 저장합니다.

```sql
CREATE TABLE skills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  github_url VARCHAR(500) NOT NULL,
  category_path JSONB DEFAULT '[]'::jsonb,
  tags JSONB DEFAULT '[]'::jsonb,
  memo TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_skills_user_id ON skills(user_id);
CREATE INDEX idx_skills_created_at ON skills(created_at DESC);
CREATE INDEX idx_skills_title ON skills(title);
CREATE INDEX idx_skills_category_path ON skills(category_path);
CREATE INDEX idx_skills_tags ON skills USING GIN(tags);

-- 전체 텍스트 검색 인덱스 (선택적)
CREATE INDEX idx_skills_search ON skills USING GIN(
  to_tsvector('english', title || ' ' || COALESCE(description, ''))
);
```

**필드 설명:**
- `id`: SKILL 고유 식별자
- `user_id`: 등록한 사용자 ID (외래키)
- `title`: SKILL 이름 (SKILL.md의 name)
- `description`: SKILL 설명 (SKILL.md의 description)
- `github_url`: GitHub 저장소 URL
- `category_path`: 카테고리 계층 구조 (JSONB 배열, 예: `["개발", "프론트엔드", "React"]`)
- `tags`: 태그 배열 (JSONB, 예: `["react", "hooks", "optimization"]`)
- `memo`: 사용자 개인 메모 (선택적)
- `created_at`: 등록 시간
- `updated_at`: 마지막 수정 시간

**category_path 형식:**
```json
["개발"]
["개발", "프론트엔드"]
["개발", "프론트엔드", "React", "Hooks", "최적화"]
```

**tags 형식:**
```json
["react", "typescript", "hooks"]
```

---

### 3. favorites 테이블

사용자의 즐겨찾기 정보를 저장합니다.

```sql
CREATE TABLE favorites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, skill_id)
);

-- 인덱스
CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_skill_id ON favorites(skill_id);
CREATE INDEX idx_favorites_created_at ON favorites(created_at DESC);
```

**필드 설명:**
- `id`: 즐겨찾기 고유 식별자
- `user_id`: 즐겨찾기한 사용자 ID
- `skill_id`: 즐겨찾기된 SKILL ID
- `created_at`: 즐겨찾기 추가 시간

**제약 조건:**
- `UNIQUE(user_id, skill_id)`: 같은 사용자가 같은 SKILL을 중복 즐겨찾기 불가

---

### 4. shared_skills 테이블

SKILL 공유 정보를 저장합니다.

```sql
CREATE TABLE shared_skills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  from_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  to_user_email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_shared_skills_to_user_email ON shared_skills(to_user_email);
CREATE INDEX idx_shared_skills_skill_id ON shared_skills(skill_id);
CREATE INDEX idx_shared_skills_from_user_id ON shared_skills(from_user_id);
```

**필드 설명:**
- `id`: 공유 고유 식별자
- `skill_id`: 공유된 SKILL ID
- `from_user_id`: 공유한 사용자 ID
- `to_user_email`: 공유받을 사용자 이메일
- `created_at`: 공유 시간

**참고:**
- `to_user_email`은 users 테이블의 email과 조인하여 사용
- 같은 SKILL을 여러 사용자에게 공유 가능 (중복 허용)
- 같은 SKILL을 같은 사람에게 여러 번 공유 가능 (중복 허용)
- 공유받은 SKILL은 받은 사람의 독립적인 SKILL로 관리됨

---

## 주요 쿼리 예시

### 1. 전체 SKILLS 조회 (즐겨찾기 수 포함)
```sql
SELECT 
  s.*,
  u.email as author_email,
  COUNT(f.id) as favorite_count,
  EXISTS(
    SELECT 1 FROM favorites 
    WHERE user_id = $current_user_id AND skill_id = s.id
  ) as is_favorited
FROM skills s
LEFT JOIN users u ON s.user_id = u.id
LEFT JOIN favorites f ON s.id = f.skill_id
GROUP BY s.id, u.email
ORDER BY s.created_at DESC;
```

### 2. 내 SKILLS 조회
```sql
SELECT s.*, COUNT(f.id) as favorite_count
FROM skills s
LEFT JOIN favorites f ON s.id = f.skill_id
WHERE s.user_id = $current_user_id
GROUP BY s.id
ORDER BY s.created_at DESC;
```

### 3. 공유받은 SKILLS 조회
```sql
SELECT 
  s.*,
  u.email as author_email,
  ss.from_user_id,
  fu.email as shared_from_email,
  COUNT(f.id) as favorite_count
FROM shared_skills ss
JOIN skills s ON ss.skill_id = s.id
JOIN users u ON s.user_id = u.id
JOIN users fu ON ss.from_user_id = fu.id
LEFT JOIN favorites f ON s.id = f.skill_id
WHERE ss.to_user_email = $current_user_email
GROUP BY s.id, u.email, ss.from_user_id, fu.email
ORDER BY ss.created_at DESC;
```

### 4. 카테고리 필터링 (하위 카테고리 포함)
```sql
SELECT s.*, COUNT(f.id) as favorite_count
FROM skills s
LEFT JOIN favorites f ON s.id = f.skill_id
WHERE s.category_path @> $category_array::jsonb
-- 예: '["개발", "프론트엔드"]'::jsonb → '개발 > 프론트엔드' 및 하위 모두 포함
GROUP BY s.id
ORDER BY s.created_at DESC;
```

### 5. 검색 (이름, 설명, 카테고리, 태그)
```sql
SELECT s.*, COUNT(f.id) as favorite_count
FROM skills s
LEFT JOIN favorites f ON s.id = f.skill_id
WHERE 
  s.title ILIKE '%' || $search_query || '%'
  OR s.description ILIKE '%' || $search_query || '%'
  OR s.category_path::text ILIKE '%' || $search_query || '%'
  OR EXISTS (
    SELECT 1 FROM jsonb_array_elements_text(s.tags) AS tag
    WHERE tag ILIKE '%' || $search_query || '%'
  )
GROUP BY s.id
ORDER BY s.created_at DESC;
```

### 6. 즐겨찾기 추가
```sql
INSERT INTO favorites (user_id, skill_id)
VALUES ($user_id, $skill_id)
ON CONFLICT (user_id, skill_id) DO NOTHING;
```

### 7. SKILL 복사
```sql
INSERT INTO skills (user_id, title, description, github_url, category_path, tags, memo)
SELECT 
  $new_user_id,
  title,
  description,
  github_url,
  category_path,
  tags,
  NULL -- memo는 복사하지 않음
FROM skills
WHERE id = $original_skill_id;
```

### 8. SKILL 공유
```sql
INSERT INTO shared_skills (skill_id, from_user_id, to_user_email)
VALUES ($skill_id, $from_user_id, $to_user_email);
```

### 9. 관리자 - 전체 사용자 조회
```sql
SELECT 
  u.id,
  u.email,
  u.role,
  u.is_active,
  u.created_at,
  COUNT(DISTINCT s.id) as skill_count,
  COUNT(DISTINCT f.id) as favorite_count
FROM users u
LEFT JOIN skills s ON u.id = s.user_id
LEFT JOIN favorites f ON u.id = f.user_id
GROUP BY u.id, u.email, u.role, u.is_active, u.created_at
ORDER BY u.created_at DESC;
```

### 10. 관리자 - 사용자 역할 변경
```sql
UPDATE users
SET role = $new_role
WHERE id = $user_id;
```

### 11. 관리자 - 전체 통계
```sql
SELECT 
  (SELECT COUNT(*) FROM users WHERE is_active = true) as total_users,
  (SELECT COUNT(*) FROM skills) as total_skills,
  (SELECT COUNT(*) FROM favorites) as total_favorites,
  (SELECT COUNT(*) FROM shared_skills) as total_shares;
```

### 12. 관리자 - 인기 SKILL Top 10
```sql
SELECT 
  s.*,
  u.email as author_email,
  COUNT(f.id) as favorite_count
FROM skills s
JOIN users u ON s.user_id = u.id
LEFT JOIN favorites f ON s.id = f.skill_id
GROUP BY s.id, u.email
ORDER BY favorite_count DESC
LIMIT 10;
```

---

## RLS (Row Level Security) 정책

Supabase의 RLS를 활용하여 보안을 강화합니다.

### skills 테이블
```sql
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
```

### favorites 테이블
```sql
-- 본인의 즐겨찾기만 조회 가능
CREATE POLICY "Users can view own favorites"
ON favorites FOR SELECT
USING (auth.uid() = user_id);

-- 본인의 즐겨찾기만 추가 가능
CREATE POLICY "Users can insert own favorites"
ON favorites FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- 본인의 즐겨찾기만 삭제 가능
CREATE POLICY "Users can delete own favorites"
ON favorites FOR DELETE
USING (auth.uid() = user_id);
```

### shared_skills 테이블
```sql
-- 본인이 공유한 것 또는 본인에게 공유된 것만 조회
CREATE POLICY "Users can view relevant shared skills"
ON shared_skills FOR SELECT
USING (
  auth.uid() = from_user_id 
  OR to_user_email = (SELECT email FROM users WHERE id = auth.uid())
);

-- 본인의 SKILL만 공유 가능
CREATE POLICY "Users can share own skills"
ON shared_skills FOR INSERT
WITH CHECK (
  auth.uid() = from_user_id
  AND EXISTS (SELECT 1 FROM skills WHERE id = skill_id AND user_id = auth.uid())
);
```

---

## 마이그레이션 순서

1. `users` 테이블 생성
2. `skills` 테이블 생성
3. `favorites` 테이블 생성
4. `shared_skills` 테이블 생성
5. 인덱스 생성
6. RLS 정책 적용

---

## 향후 확장 고려사항

### Phase 2 고도화 시 추가 가능한 테이블

#### skill_versions (버전 관리)
```sql
CREATE TABLE skill_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  version_number INT NOT NULL,
  title VARCHAR(255),
  description TEXT,
  category_path VARCHAR(500),
  tags JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### notifications (알림)
```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL, -- 'shared', 'forked', etc.
  message TEXT,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### skill_relationships (GraphDB 대체)
```sql
CREATE TABLE skill_relationships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  from_skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  to_skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  relationship_type VARCHAR(50), -- 'depends_on', 'similar_to', 'extends'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```
