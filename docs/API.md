# API 초안

서버 실행 후 Swagger UI는 `http://127.0.0.1:8000/docs`에서 확인할 수 있습니다.

| Method | Path | 설명 |
| --- | --- | --- |
| `GET` | `/health` | 서버 상태 확인 |
| `POST` | `/api/v1/items` | 분실물 접수 |
| `GET` | `/api/v1/items` | 분실물 목록·검색 (`status`, `category`, `keyword`) |
| `GET` | `/api/v1/items/{item_id}` | 분실물 상세 조회 |
| `PATCH` | `/api/v1/items/{item_id}/status` | 보관·수령 상태 변경 |

`status` 값은 `received`(접수), `stored`(보관), `claimed`(수령 완료)입니다.
