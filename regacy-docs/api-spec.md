# API 명세서

## 기본 정보

- **Base URL**: `/api`
- **인증 방식**: Supabase Auth (JWT Token)
- **Content-Type**: `application/json`
- **에러 응답 형식**:
  ```json
  {
    "error": {
      "code": "ERROR_CODE",
      "message": "사용자 친화적인 에러 메시지"
    }
  }
  ```

---

## 인증 (Authentication)

### 1. 회원가입
```
POST /api/auth/signup
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "created_at": "2026-01-28T10:00:00Z"
  },
  "session": {
    "access_token": "jwt_token",
    "refresh_token": "refresh_token"
  }
}
```

**Errors:**
- `400 EMAIL_INVALID`: 이메일 형식이 올바르지 않습니다
- `400 PASSWORD_TOO_SHORT`: 비밀번호는 최소 8자 이상이어야 합니다
- `409 EMAIL_EXISTS`: 이미 가입된 이메일입니다

---

### 2. 로그인
```
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  },
  "session": {
    "access_token": "jwt_token",
    "refresh_token": "refresh_token"
  }
}
```

**Errors:**
- `401 INVALID_CREDENTIALS`: 이메일 또는 비밀번호가 올바르지 않습니다

---

### 3. 로그아웃
```
POST /api/auth/logout
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "로그아웃되었습니다"
}
```

---

## SKILL 관리

### 1. SKILL 목록 조회
```
GET /api/skills
```

**Query Parameters:**
- `tab` (string): `all` | `my` | `shared` (기본값: `all`)
- `search` (string, optional): 검색어
- `category` (string, optional): 카테고리 경로 (예: `["개발", "프론트엔드"]`)
- `tag` (string, optional): 태그 (예: `react`)
- `sort` (string): `latest` | `oldest` | `name` | `favorites` (기본값: `latest`)
- `page` (number): 페이지 번호 (기본값: 1)
- `limit` (number): 페이지당 항목 수 (기본값: 12)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "skills": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "title": "Frontend Design",
      "description": "A comprehensive guide...",
      "github_url": "https://github.com/...",
      "category_path": ["개발", "프론트엔드", "UI"],
      "tags": ["design", "ui", "frontend"],
      "created_at": "2026-01-28T10:00:00Z",
      "updated_at": "2026-01-28T10:00:00Z",
      "author_email": "user@example.com",
      "favorite_count": 5,
      "is_favorited": true
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 60,
    "items_per_page": 12
  }
}
```

**Errors:**
- `401 UNAUTHORIZED`: 로그인이 필요합니다

---

### 2. SKILL 상세 조회
```
GET /api/skills/{id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Frontend Design",
  "description": "A comprehensive guide for modern UI/UX design...",
  "github_url": "https://github.com/anthropics/claude-code/...",
  "category_path": ["개발", "프론트엔드", "UI"],
  "tags": ["design", "ui", "frontend", "ux"],
  "memo": "나중에 프로젝트에 적용해보기",
  "created_at": "2026-01-28T10:00:00Z",
  "updated_at": "2026-01-28T10:00:00Z",
  "author_email": "user@example.com",
  "favorite_count": 5,
  "is_favorited": true,
  "is_owner": false
}
```

**Errors:**
- `404 SKILL_NOT_FOUND`: SKILL을 찾을 수 없습니다

---

### 3. SKILL 등록
```
POST /api/skills
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "github_url": "https://github.com/anthropics/claude-code/...",
  "title": "Frontend Design",
  "description": "A comprehensive guide...",
  "category_path": ["개발", "프론트엔드", "UI"],
  "tags": ["design", "ui", "frontend"],
  "memo": "나중에 프로젝트에 적용해보기"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Frontend Design",
  "description": "A comprehensive guide...",
  "github_url": "https://github.com/...",
  "category_path": ["개발", "프론트엔드", "UI"],
  "tags": ["design", "ui", "frontend"],
  "memo": "나중에 프로젝트에 적용해보기",
  "created_at": "2026-01-28T10:00:00Z",
  "updated_at": "2026-01-28T10:00:00Z"
}
```

**Errors:**
- `400 INVALID_URL`: GitHub URL 형식이 올바르지 않습니다
- `401 UNAUTHORIZED`: 로그인이 필요합니다

---

### 4. SKILL 수정
```
PATCH /api/skills/{id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description...",
  "category_path": ["개발", "백엔드"],
  "tags": ["backend", "api"],
  "memo": "수정된 메모"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Updated Title",
  "description": "Updated description...",
  "github_url": "https://github.com/...",
  "category_path": ["개발", "백엔드"],
  "tags": ["backend", "api"],
  "memo": "수정된 메모",
  "created_at": "2026-01-28T10:00:00Z",
  "updated_at": "2026-01-28T11:00:00Z"
}
```

**Errors:**
- `403 FORBIDDEN`: 본인이 등록한 SKILL만 수정할 수 있습니다
- `404 SKILL_NOT_FOUND`: SKILL을 찾을 수 없습니다

---

### 5. SKILL 삭제
```
DELETE /api/skills/{id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "SKILL이 삭제되었습니다"
}
```

**Errors:**
- `403 FORBIDDEN`: 본인이 등록한 SKILL만 삭제할 수 있습니다
- `404 SKILL_NOT_FOUND`: SKILL을 찾을 수 없습니다

---

### 6. SKILL 복사
```
POST /api/skills/{id}/copy
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (201 Created):**
```json
{
  "id": "new_uuid",
  "user_id": "current_user_uuid",
  "title": "Frontend Design",
  "description": "A comprehensive guide...",
  "github_url": "https://github.com/...",
  "category_path": ["개발", "프론트엔드", "UI"],
  "tags": ["design", "ui", "frontend"],
  "memo": null,
  "created_at": "2026-01-28T12:00:00Z",
  "updated_at": "2026-01-28T12:00:00Z"
}
```

**Errors:**
- `404 SKILL_NOT_FOUND`: SKILL을 찾을 수 없습니다

---

## GitHub 연동

### 1. GitHub SKILL 정보 가져오기
```
POST /api/github/fetch-skill
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "github_url": "https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design/skills/frontend-design"
}
```

**Response (200 OK):**
```json
{
  "title": "Frontend Design",
  "description": "A comprehensive guide for modern UI/UX design principles and best practices.",
  "github_url": "https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design/skills/frontend-design"
}
```

**Errors:**
- `400 INVALID_URL`: GitHub URL 형식이 올바르지 않습니다
- `404 REPO_NOT_FOUND`: GitHub 저장소를 찾을 수 없습니다. URL을 확인해주세요.
- `404 SKILL_FILE_NOT_FOUND`: SKILL.md 파일을 찾을 수 없습니다. 올바른 SKILL 경로인지 확인해주세요.
- `400 INVALID_YAML`: SKILL.md의 형식이 올바르지 않습니다. name과 description을 확인해주세요.

---

## AI 추천

### 1. 카테고리/태그 추천
```
POST /api/ai/recommend
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Frontend Design",
  "description": "A comprehensive guide for modern UI/UX design principles and best practices.",
  "user_id": "uuid"
}
```

**Response (200 OK):**
```json
{
  "category_path": ["개발", "프론트엔드", "UI"],
  "tags": ["design", "ui", "frontend", "ux"]
}
```

**Errors:**
- `500 AI_SERVICE_UNAVAILABLE`: AI 추천 서비스가 일시적으로 사용 불가합니다. 수동으로 입력해주세요.
- `429 RATE_LIMIT_EXCEEDED`: AI 추천 서비스가 일시적으로 사용 불가합니다. 수동으로 입력해주세요.
- `500 AI_ERROR`: AI 추천을 가져오는 중 오류가 발생했습니다. 재시도 버튼을 눌러주세요.

---

## 즐겨찾기

### 1. 즐겨찾기 추가
```
POST /api/favorites
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "skill_id": "uuid"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "skill_id": "uuid",
  "created_at": "2026-01-28T10:00:00Z"
}
```

**Errors:**
- `404 SKILL_NOT_FOUND`: SKILL을 찾을 수 없습니다
- `409 ALREADY_FAVORITED`: 이미 즐겨찾기한 SKILL입니다

---

### 2. 즐겨찾기 제거
```
DELETE /api/favorites/{skill_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "즐겨찾기가 제거되었습니다"
}
```

**Errors:**
- `404 FAVORITE_NOT_FOUND`: 즐겨찾기를 찾을 수 없습니다

---

## 공유

### 1. SKILL 공유
```
POST /api/skills/{id}/share
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "to_user_email": "recipient@example.com"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "skill_id": "uuid",
  "from_user_id": "uuid",
  "to_user_email": "recipient@example.com",
  "created_at": "2026-01-28T10:00:00Z"
}
```

**Errors:**
- `400 INVALID_EMAIL`: 이메일 형식이 올바르지 않습니다
- `403 FORBIDDEN`: 본인이 등록한 SKILL만 공유할 수 있습니다
- `404 USER_NOT_FOUND`: 해당 이메일로 가입된 사용자가 없습니다
- `400 SELF_SHARE`: 자신에게는 SKILL을 공유할 수 없습니다
- `404 SKILL_NOT_FOUND`: SKILL을 찾을 수 없습니다

---

### 2. 공유받은 SKILL 목록 조회
```
GET /api/shared-skills
```

**Query Parameters:**
- `page` (number): 페이지 번호 (기본값: 1)
- `limit` (number): 페이지당 항목 수 (기본값: 12)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "skills": [
    {
      "id": "uuid",
      "user_id": "original_owner_uuid",
      "title": "Frontend Design",
      "description": "A comprehensive guide...",
      "github_url": "https://github.com/...",
      "category_path": ["개발", "프론트엔드", "UI"],
      "tags": ["design", "ui", "frontend"],
      "created_at": "2026-01-28T10:00:00Z",
      "updated_at": "2026-01-28T10:00:00Z",
      "author_email": "original@example.com",
      "shared_from_email": "sharer@example.com",
      "shared_at": "2026-01-28T11:00:00Z",
      "favorite_count": 5,
      "is_favorited": false
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 3,
    "total_items": 36,
    "items_per_page": 12
  }
}
```

---

## 카테고리

### 1. 전체 카테고리 목록 조회
```
GET /api/categories
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "categories": [
    {
      "path": ["개발"],
      "count": 120
    },
    {
      "path": ["개발", "프론트엔드"],
      "count": 45
    },
    {
      "path": ["개발", "프론트엔드", "React"],
      "count": 20
    },
    {
      "path": ["개발", "백엔드"],
      "count": 35
    },
    {
      "path": ["디자인"],
      "count": 30
    }
  ]
}
```

---

## 에러 코드 정리

| 코드 | HTTP Status | 설명 |
|------|-------------|------|
| `EMAIL_INVALID` | 400 | 이메일 형식이 올바르지 않습니다 |
| `PASSWORD_TOO_SHORT` | 400 | 비밀번호는 최소 8자 이상이어야 합니다 |
| `EMAIL_EXISTS` | 409 | 이미 가입된 이메일입니다 |
| `INVALID_CREDENTIALS` | 401 | 이메일 또는 비밀번호가 올바르지 않습니다 |
| `UNAUTHORIZED` | 401 | 로그인이 필요합니다 |
| `FORBIDDEN` | 403 | 권한이 없습니다 |
| `SKILL_NOT_FOUND` | 404 | SKILL을 찾을 수 없습니다 |
| `USER_NOT_FOUND` | 404 | 사용자를 찾을 수 없습니다 |
| `INVALID_URL` | 400 | URL 형식이 올바르지 않습니다 |
| `REPO_NOT_FOUND` | 404 | GitHub 저장소를 찾을 수 없습니다 |
| `SKILL_FILE_NOT_FOUND` | 404 | SKILL.md 파일을 찾을 수 없습니다 |
| `INVALID_YAML` | 400 | YAML frontmatter 형식이 올바르지 않습니다 |
| `AI_SERVICE_UNAVAILABLE` | 500 | AI 서비스를 사용할 수 없습니다 |
| `RATE_LIMIT_EXCEEDED` | 429 | API 할당량을 초과했습니다 |
| `ALREADY_FAVORITED` | 409 | 이미 즐겨찾기한 SKILL입니다 |
| `SELF_SHARE` | 400 | 자신에게는 공유할 수 없습니다 |

---

## 인증 헤더 예시

모든 보호된 엔드포인트는 다음 헤더가 필요합니다:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Supabase Auth에서 발급한 JWT 토큰을 사용합니다.
