# API Contract (MVP v1)

## 공통
- Base: `/api`
- Auth: 세션 기반 인증(미인증 401)
- Content-Type: `application/json`
- 에러 형식:
```json
{
  "code": "bad_request:api",
  "message": "The request couldn't be processed.",
  "cause": "optional detail"
}
```

## 1) Skills

### GET `/api/skills`
### Query
- `search?: string`
- `limit?: number` (default 20, max 100)

### Response 200
```json
{
  "skills": [
    {
      "id": "uuid",
      "title": "Frontend Design Skill",
      "description": "Reusable workflow",
      "githubUrl": "https://github.com/org/repo",
      "tags": ["frontend", "design"],
      "ownerId": "uuid",
      "createdAt": "2026-02-22T00:00:00.000Z",
      "updatedAt": "2026-02-22T00:00:00.000Z"
    }
  ]
}
```

### POST `/api/skills`
### Body
```json
{
  "title": "Frontend Design Skill",
  "description": "Reusable workflow",
  "githubUrl": "https://github.com/org/repo",
  "tags": ["frontend", "design"]
}
```

### Response 201
```json
{
  "skill": {
    "id": "uuid",
    "title": "Frontend Design Skill",
    "description": "Reusable workflow",
    "githubUrl": "https://github.com/org/repo",
    "tags": ["frontend", "design"],
    "ownerId": "uuid",
    "createdAt": "2026-02-22T00:00:00.000Z",
    "updatedAt": "2026-02-22T00:00:00.000Z"
  }
}
```

---

## 2) Providers

### GET `/api/providers`
- 연결된 provider 목록과 상태 반환

### POST `/api/providers`
- provider 연결 생성/검증

### PATCH `/api/providers/:id`
- 연결 상태 변경(재연결/비활성화)

---

## 3) Install Runs

### POST `/api/install-runs`
### Body
```json
{
  "action": "install",
  "skillId": "uuid",
  "providerIds": ["uuid", "uuid"],
  "requestedRef": "main"
}
```

### Response 202
```json
{
  "runIds": ["uuid", "uuid"],
  "status": "queued"
}
```

### GET `/api/install-runs`
### Query
- `skillId?: uuid`
- `providerId?: uuid`
- `status?: queued|running|success|failed|partial_failed`
- `limit?: number`

### Response 200
```json
{
  "runs": [
    {
      "id": "uuid",
      "skillId": "uuid",
      "providerId": "uuid",
      "action": "install",
      "status": "running",
      "attempt": 1,
      "errorCode": null,
      "errorMessage": null,
      "startedAt": "2026-02-22T00:00:00.000Z",
      "finishedAt": null
    }
  ]
}
```

---

## 4) Chat Ops

### POST `/api/chat-ops`
### Body
```json
{
  "input": "Skill A를 전체 provider에 설치해줘"
}
```

### Response 200
```json
{
  "intent": "bulk_install",
  "resolvedAction": {
    "skillId": "uuid",
    "providerScope": "all",
    "action": "install",
    "ref": "main"
  },
  "accepted": true,
  "runIds": ["uuid", "uuid", "uuid"]
}
```

### 규칙
- 자연어 입력은 즉시 실행하지 않고 파라미터 검증 후 실행
- 실행 불가 시 `accepted: false` + 원인 반환

---

## 상태/코드 표준
- Run Status: `queued | running | success | failed | partial_failed`
- Error Code 예시:
  - `bad_request:api`
  - `unauthorized:auth`
  - `forbidden:auth`
  - `bad_request:database`
  - `not_found:skill`
  - `bad_request:provider`

