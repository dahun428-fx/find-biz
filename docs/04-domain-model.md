# Domain Model (MVP v1)

## 목적
- Skill 관리에서 시작해, 향후 "나의 AI 운영 플랫폼"으로 확장 가능한 도메인 모델을 정의한다.
- MVP에서는 최소 엔터티만 도입하고, 확장 필드는 Reserved로 둔다.

## 엔터티 개요
1. `users`
2. `skills`
3. `providers`
4. `install_targets`
5. `install_runs`
6. `chat_actions`

---

## 1) users
### 역할
- 인증 사용자 및 권한(일반/관리자) 관리

### 필드(MVP)
- `id` (uuid, pk)
- `email` (varchar, unique, not null)
- `role` (enum: `user | admin`, default `user`)
- `is_active` (boolean, default true)
- `created_at` (timestamptz)

---

## 2) skills
### 역할
- GitHub 기반 Skill 원본 메타데이터 저장

### 필드(MVP)
- `id` (uuid, pk)
- `owner_id` (uuid, fk -> users.id)
- `title` (varchar(120), not null)
- `description` (text)
- `github_url` (varchar(500), not null)
- `source_ref` (varchar(120), default `main`)
- `tags` (jsonb, default `[]`)
- `is_archived` (boolean, default false)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

### 인덱스 권장
- `(owner_id, created_at desc)`
- `gin(tags)`
- `github_url`

---

## 3) providers
### 역할
- 설치 대상 AI Provider 연결 정보 관리

### 필드(MVP)
- `id` (uuid, pk)
- `owner_id` (uuid, fk -> users.id)
- `name` (enum: `openai | claude | gemini`)
- `display_name` (varchar(50))
- `status` (enum: `connected | disconnected | error`)
- `config` (jsonb)  
  - 예: workspace/project id, endpoint, region
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

### 규칙
- API key/secret은 DB plain text 저장 금지(시크릿 스토어 참조키만 저장)

---

## 4) install_targets
### 역할
- Skill과 Provider의 설치 관계(원하는 상태) 정의

### 필드(MVP)
- `id` (uuid, pk)
- `skill_id` (uuid, fk -> skills.id)
- `provider_id` (uuid, fk -> providers.id)
- `desired_ref` (varchar(120))  
  - 설치 목표 버전/태그/커밋
- `installed_ref` (varchar(120), nullable)
- `status` (enum: `idle | syncing | installed | failed`)
- `last_synced_at` (timestamptz, nullable)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

### 제약
- unique(`skill_id`, `provider_id`)

---

## 5) install_runs
### 역할
- 실제 실행된 설치/재시도/롤백 작업 이력

### 필드(MVP)
- `id` (uuid, pk)
- `skill_id` (uuid, fk -> skills.id)
- `provider_id` (uuid, fk -> providers.id)
- `target_id` (uuid, fk -> install_targets.id, nullable)
- `triggered_by` (uuid, fk -> users.id)
- `trigger_source` (enum: `ui | chatbot | system`)
- `action` (enum: `install | sync | retry | rollback`)
- `requested_ref` (varchar(120), nullable)
- `status` (enum: `queued | running | success | failed | partial_failed`)
- `attempt` (int, default 1)
- `error_code` (varchar(100), nullable)
- `error_message` (text, nullable)
- `started_at` (timestamptz, nullable)
- `finished_at` (timestamptz, nullable)
- `created_at` (timestamptz)

### 인덱스 권장
- `(created_at desc)`
- `(skill_id, provider_id, created_at desc)`
- `(status, created_at desc)`

---

## 6) chat_actions
### 역할
- 챗봇 명령에서 생성된 액션 감사 로그

### 필드(MVP)
- `id` (uuid, pk)
- `user_id` (uuid, fk -> users.id)
- `intent` (varchar(100))
- `input_text` (text)
- `resolved_action` (jsonb)  
  - 검증된 액션 파라미터
- `run_id` (uuid, fk -> install_runs.id, nullable)
- `result` (enum: `accepted | rejected | executed | failed`)
- `created_at` (timestamptz)

---

## ERD 텍스트
- `users 1:N skills`
- `users 1:N providers`
- `skills 1:N install_targets`
- `providers 1:N install_targets`
- `skills/providers 1:N install_runs`
- `users 1:N install_runs`
- `users 1:N chat_actions`
- `install_runs 1:N chat_actions (optional linkage)`

---

## Reserved (고도화)
- `skill_versions`
- `deployment_policies`
- `approval_requests`
- `cost_usage_daily`
- `drift_events`

