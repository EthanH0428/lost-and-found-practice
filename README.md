# 교내 분실물 관리 서비스

교내에서 접수된 분실물을 등록하고, 장소·분류·키워드로 찾아 수령 상태까지 관리하는 Python API의 시작 프로젝트입니다.

## 포함된 기능

- 분실물 접수, 상세 조회, 목록 검색
- 분류·상태·키워드 필터 및 페이지 단위 조회
- 접수/보관/수령 완료 상태 변경
- 개발용 SQLite 데이터베이스와 자동 테이블 생성
- OpenAPI(Swagger) 문서와 API 기본 테스트

## 시작하기

Python 3.11 이상을 준비한 뒤 다음을 실행하세요.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

실행 후 아래 주소를 이용할 수 있습니다.

- API 문서: `http://127.0.0.1:8000/docs`
- 상태 확인: `http://127.0.0.1:8000/health`

테스트는 `pytest`로 실행합니다.

## 프로젝트 구조

```text
app/
  api/          # 라우트와 요청별 DB 의존성
  core/         # 환경 설정
  db/           # 엔진·세션·ORM 기본 클래스
  models/       # SQLAlchemy 테이블 모델
  schemas/      # 요청·응답 검증 모델
  services/     # 비즈니스 규칙
  main.py       # 애플리케이션 진입점
tests/          # 자동화 테스트
docs/API.md     # 엔드포인트 요약
```

개발 중 생성되는 데이터베이스는 `data/`에 저장되며 Git에는 포함되지 않습니다. Docker로 실행하려면 `docker compose up --build`를 사용하세요.
