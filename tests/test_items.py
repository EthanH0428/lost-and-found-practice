from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def test_register_list_and_claim_item(tmp_path):
    settings = Settings(database_url=f"sqlite:///{tmp_path / 'test.db'}")
    app = create_app(settings)

    with TestClient(app) as client:
        create_response = client.post(
            "/api/v1/items",
            json={
                "title": "검은색 우산",
                "description": "공학관 1층에 놓여 있던 검은색 접이식 우산입니다.",
                "category": "etc",
                "found_location": "공학관 1층 안내데스크",
                "found_at": datetime.now(timezone.utc).isoformat(),
                "reporter_name": "홍길동",
                "reporter_contact": "student@example.ac.kr",
            },
        )
        assert create_response.status_code == 201
        item_id = create_response.json()["id"]

        list_response = client.get("/api/v1/items", params={"keyword": "우산"})
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        claim_response = client.patch(
            f"/api/v1/items/{item_id}/status", json={"status": "claimed"}
        )
        assert claim_response.status_code == 200
        assert claim_response.json()["claimed_at"] is not None
