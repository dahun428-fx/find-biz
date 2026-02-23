# Provider Adapter Spec (MVP)

## 목적
- Gemini/OpenAI/Claude를 공통 인터페이스로 다루기 위한 어댑터 계약을 정의한다.

## 설계 원칙
- 앱 코드는 provider별 SDK를 직접 호출하지 않는다.
- 모든 실행은 `ProviderAdapter` 인터페이스를 통해 수행한다.
- 공통 입력/출력 포맷을 사용해 UI/챗봇/잡 처리 로직을 단순화한다.

## TypeScript 인터페이스 (초안)
```ts
type InstallAction = "install" | "sync" | "retry" | "rollback";

type ProviderExecutionInput = {
  skillId: string;
  requestedRef?: string;
  action: InstallAction;
  metadata?: Record<string, unknown>;
};

type ProviderExecutionResult = {
  ok: boolean;
  providerRunId?: string;
  installedRef?: string;
  errorCode?: string;
  errorMessage?: string;
};

interface ProviderAdapter {
  readonly name: "openai" | "claude" | "gemini";
  validateConnection(): Promise<{ ok: boolean; reason?: string }>;
  installSkill(input: ProviderExecutionInput): Promise<ProviderExecutionResult>;
  getInstallStatus(input: {
    skillId: string;
  }): Promise<{ status: "installed" | "not_installed" | "unknown"; installedRef?: string }>;
}
```

## 어댑터 레지스트리
- 위치: `lib/providers/registry.ts`
- 역할:
1. provider name으로 adapter resolve
2. 미지원 provider 요청 시 공통 에러 반환

## 에러 매핑 규칙
- SDK/HTTP 에러를 내부 코드로 정규화:
  - `provider_auth_error`
  - `provider_rate_limited`
  - `provider_timeout`
  - `provider_invalid_request`
  - `provider_unknown_error`

## 기능 매트릭스 (MVP)
- OpenAI: `validateConnection`, `installSkill`, `getInstallStatus`
- Claude: `validateConnection`, `installSkill`, `getInstallStatus`
- Gemini: `validateConnection`, `installSkill`, `getInstallStatus`

## 버전/참조 규칙
- `requestedRef` 우선순위:
1. API 입력 ref
2. skill.source_ref
3. 기본 `main`

## 보안 규칙
- adapter는 plain API key를 로그에 출력하지 않는다.
- provider 요청/응답 원문 로그는 마스킹 후 저장한다.
- 자격증명은 adapter 생성 시점에 시크릿 스토어에서 로드한다.

## 확장 포인트
- 추후 provider별 capability 추가:
  - `supportsRollback`
  - `supportsDryRun`
  - `supportsBulkInstall`

