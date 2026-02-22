# API 명세서 - 관리자 API 추가

## 관리자 API

### 1. 사용자 목록 조회 (관리자)
```
GET /api/admin/users
```

**Headers:**
```
Authorization: Bearer {access_token}
X-User-Role: admin
```

**Query Parameters:**
- `search` (string, optional): 이메일 검색
- `role` (string, optional): `user` | `admin` | `all` (기본값: `all`)
- `is_active` (boolean, optional): 활성화 상태 필터
- `page` (number): 페이지 번호 (기본값: 1)
- `limit` (number): 페이지당 항목 수 (기본값: 20)

**Response (200 OK):**
```json
{
  "users": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "role": "user",
      "is_active": true,
      "created_at": "2026-01-28T10:00:00Z",
      "skill_count": 5,
      "favorite_count": 12
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 20
  }
}
```

**Errors:**
- `403 FORBIDDEN`: 관리자 권한이 필요합니다

---

### 2. 사용자 역할 변경 (관리자)
```
PATCH /api/admin/users/{user_id}/role
```

**Headers:**
```
Authorization: Bearer {access_token}
X-User-Role: admin
```

**Request Body:**
```json
{
  "role": "admin"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "role": "admin",
  "is_active": true,
  "updated_at": "2026-01-28T11:00:00Z"
}
```

**Errors:**
- `403 FORBIDDEN`: 관리자 권한이 필요합니다
- `404 USER_NOT_FOUND`: 사용자를 찾을 수 없습니다
- `400 INVALID_ROLE`: 유효하지 않은 역할입니다

---

### 3. 사용자 계정 정지/활성화 (관리자)
```
PATCH /api/admin/users/{user_id}/status
```

**Headers:**
```
Authorization: Bearer {access_token}
X-User-Role: admin
```

**Request Body:**
```json
{
  "is_active": false
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": false,
  "updated_at": "2026-01-28T11:00:00Z"
}
```

**Errors:**
- `403 FORBIDDEN`: 관리자 권한이 필요합니다
- `404 USER_NOT_FOUND`: 사용자를 찾을 수 없습니다

---

### 4. 사용자 계정 삭제 (관리자)
```
DELETE /api/admin/users/{user_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
X-User-Role: admin
```

**Response (200 OK):**
```json
{
  "message": "사용자 계정이 삭제되었습니다"
}
```

**Errors:**
- `403 FORBIDDEN`: 관리자 권한이 필요합니다
- `404 USER_NOT_FOUND`: 사용자를 찾을 수 없습니다
- `400 CANNOT_DELETE_SELF`: 자신의 계정은 삭제할 수 없습니다

---

### 5. 전체 SKILL 목록 조회 (관리자)
```
GET /api/admin/skills
```

**Headers:**
```
Authorization: Bearer {access_token}
X-User-Role: admin
```

**Query Parameters:**
- `search` (string, optional): 검색어
- `user_id` (string, optional): 특정 사용자의 SKILL만
- `page` (number): 페이지 번호 (기본값: 1)
- `limit` (number): 페이지당 항목 수 (기본값: 20)

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
      "author_email": "user@example.com",
      "favorite_count": 5
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 200,
    "items_per_page": 20
  }
}
```

---

### 6. SKILL 수정 (관리자)
```
PATCH /api/admin/skills/{skill_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
X-User-Role: admin
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description...",
  "category_path": ["개발", "백엔드"],
  "tags": ["backend", "api"]
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "title": "Updated Title",
  "description": "Updated description...",
  "updated_at": "2026-01-28T11:00:00Z"
}
```

---

### 7. SKILL 삭제 (관리자)
```
DELETE /api/admin/skills/{skill_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
X-User-Role: admin
```

**Response (200 OK):**
```json
{
  "message": "SKILL이 삭제되었습니다"
}
```

---

### 8. 전체 통계 조회 (관리자)
```
GET /api/admin/stats
```

**Headers:**
```
Authorization: Bearer {access_token}
X-User-Role: admin
```

**Response (200 OK):**
```json
{
  "total_users": 150,
  "total_skills": 320,
  "total_favorites": 1250,
  "total_shares": 85,
  "recent_users": [
    {
      "id": "uuid",
      "email": "newuser@example.com",
      "created_at": "2026-01-28T10:00:00Z"
    }
  ],
  "recent_skills": [
    {
      "id": "uuid",
      "title": "New SKILL",
      "author_email": "user@example.com",
      "created_at": "2026-01-28T09:00:00Z"
    }
  ],
  "popular_skills": [
    {
      "id": "uuid",
      "title": "Popular SKILL",
      "favorite_count": 45,
      "author_email": "user@example.com"
    }
  ]
}
```

---

## 에러 코드 추가

| 코드 | HTTP Status | 설명 |
|------|-------------|------|
| `ADMIN_REQUIRED` | 403 | 관리자 권한이 필요합니다 |
| `INVALID_ROLE` | 400 | 유효하지 않은 역할입니다 |
| `CANNOT_DELETE_SELF` | 400 | 자신의 계정은 삭제할 수 없습니다 |
| `ACCOUNT_SUSPENDED` | 403 | 계정이 정지되었습니다 |
