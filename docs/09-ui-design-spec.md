# UI Design Spec (MVP v1)

## 1. 범위
- 화면 범위: `Dashboard`, `Skill` (2개)
- 목적: 운영 요약 + Skill 관리 실행을 한 사이클로 연결

## 2. 정보 구조
- 상단 글로벌 탭: `Dashboard | Skill`
- 우측 상단 공통 액션: `챗봇 열기`, `사용자 메뉴`

---

## 3. Screen A: Dashboard (`/dashboard`)

### 3.1 레이아웃
1. `Header`
- 로고/서비스명: `AI Ops Platform`
- 탭 네비게이션: Dashboard(활성), Skill
- 우측: 챗봇 버튼, 사용자 드롭다운

2. `KPI Row` (4 cards)
- Total Skills
- Connected Providers
- Install Success (24h)
- Failed Runs

3. `Recent Runs Panel`
- 최근 실행 이력 테이블
- 컬럼: 시각, Skill, Provider, Action, Status, Duration

4. `Quick Actions Panel`
- 버튼: `전체 동기화`, `실패 재시도`, `Skill 화면으로 이동`

### 3.2 상태 정의
- Loading: 카드 스켈레톤 + 테이블 스켈레톤
- Empty: "아직 실행 이력이 없습니다"
- Error: "대시보드 데이터를 불러오지 못했습니다. 다시 시도"

### 3.3 인터랙션
- KPI 카드 클릭 -> 관련 필터가 적용된 Skill 화면 이동
- 실패 재시도 클릭 -> 확인 모달 -> 실행 큐 등록
- 챗봇 버튼 -> 우측 슬라이드 패널 오픈

---

## 4. Screen B: Skill (`/skills`)

### 4.1 레이아웃
1. `Top Control Bar`
- 검색 입력 (`이름/태그/GitHub URL`)
- 필터 (`상태`, `Provider`)
- 정렬 (`최신 업데이트`, `이름`, `실패 우선`)
- 액션 버튼: `새 Skill 등록`, `일괄 설치`, `일괄 동기화`

2. `Main Split`
- 좌측: Skill 목록(List)
- 우측: 선택 Skill 상세(Detail)

3. `Detail Sections`
- 기본 정보: 제목, 설명, GitHub URL, ref
- 설치 상태: provider별 status badge
- 실행 이력: 최근 run list
- 액션: 단일 설치, 재시도, 롤백

### 4.2 상태 정의
- Loading: 목록/상세 스켈레톤
- Empty: "등록된 Skill이 없습니다. 새 Skill을 등록하세요"
- Detail Empty: "좌측에서 Skill을 선택하세요"
- Error: 섹션별 인라인 오류 메시지

### 4.3 인터랙션
- 목록 아이템 클릭 -> 우측 상세 갱신
- 다중 Provider 선택 설치 -> 실행 확인 모달
- 롤백 클릭 -> 버전 선택 드롭다운 + 확인

---

## 5. 모달/패널 스펙

### 5.1 새 Skill 등록 모달
- 필드: GitHub URL(필수), Title(자동/수정), Description, Tags
- 버튼: `등록`, `취소`
- 검증: URL 형식, 제목 길이, 태그 개수

### 5.2 실행 확인 모달
- 대상 Skill/Provider/Action 요약
- 버튼: `실행`, `취소`

### 5.3 챗봇 패널
- 입력창 + 추천 명령 버튼
- 실행 결과를 구조화된 카드로 표시:
  - Intent
  - Resolved Action
  - Run 생성 결과

---

## 6. 컴포넌트 트리
- `PlatformLayout`
- `TopNav`
- `DashboardPage`
- `KpiCards`
- `RecentRunsTable`
- `QuickActions`
- `SkillsPage`
- `SkillsControlBar`
- `SkillList`
- `SkillDetail`
- `InstallStatusGrid`
- `RunHistoryList`
- `CreateSkillModal`
- `ConfirmRunModal`
- `OpsChatPanel`

---

## 7. 반응형 규칙
- Desktop (>=1024): Skill 화면 2단 분할(목록/상세)
- Tablet (768~1023): 상세 패널을 하단 탭으로 전환
- Mobile (<768): 단일 컬럼, 상세는 별도 시트/페이지로 표시

---

## 8. 디자인 토큰 (초안)
- Spacing: 4 / 8 / 12 / 16 / 24
- Radius: card 12, button 8
- 상태 색상:
  - success: green
  - failed: red
  - running: blue
  - queued: gray

---

## 9. 접근성 체크리스트
- 모든 아이콘 버튼에 `aria-label`
- 모달 열림 시 포커스 트랩
- 키보드로 목록 탐색 가능
- 상태 변화 시 스크린리더 문구 제공

---

## 10. MVP 제외
- 고급 그래프 대시보드
- 커스텀 테마/브랜드 스킨
- 드래그앤드롭 레이아웃 커스터마이징

