# Backend (Python)

FastAPI 기반의 백엔드 스캐폴딩입니다.

## 빠른 시작
1. 가상환경 생성
```bash
python -m venv .venv
source .venv/bin/activate
```
2. 의존성 설치
```bash
pip install -e .[dev]
```
3. 서버 실행
```bash
make run
```
4. 헬스체크
```bash
curl http://localhost:8000/health
```

## 엔드포인트
- `GET /health`
- `GET/POST /api/skills`
- `GET/POST/PATCH /api/providers`
- `POST/GET /api/install-runs`
- `POST /api/chat-ops`

## 현재 상태
- API 계약 기반 라우트/스키마/에러 포맷 최소 구현 완료
- 저장소는 인메모리(`app/services/store.py`)로 동작
- Alembic 초기 골격 포함(`alembic.ini`, `alembic/`)

## 다음 단계
1. SQLAlchemy 모델 + Alembic 첫 마이그레이션 작성
2. 인메모리 저장소를 DB 리포지토리로 교체
3. 워커(예: RQ/Celery) 연결 및 상태전이 자동화
4. provider adapter(OpenAI 우선) 구현
