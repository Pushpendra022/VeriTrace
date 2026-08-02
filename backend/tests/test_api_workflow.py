from fastapi.testclient import TestClient

from app.main import app


def test_upload_claim_and_error_structure() -> None:
    with TestClient(app) as client:
        upload = client.post("/api/documents", files={"file": ("summary.txt", b"Revenue reached $11.4 million.", "text/plain")})
        assert upload.status_code == 201
        document_id = upload.json()["id"]
        assert upload.json()["pages"][0]["page_number"] == 1
        claim = client.post(f"/api/documents/{document_id}/claims", json={"claim_text": "Revenue reached $11.4 million.", "category": "financial", "importance": "high"})
        assert claim.status_code == 201
        missing = client.get("/api/documents/does-not-exist")
        assert missing.status_code == 404 and set(missing.json()["error"]) == {"code", "message", "details"}


def test_sample_verification_and_history() -> None:
    with TestClient(app) as client:
        sample = client.post("/api/samples/contradicted/load").json()
        result = client.post(f"/api/claims/{sample['claims'][0]['id']}/verify")
        assert result.status_code == 200
        assert result.json()["verdict"] == "CONTRADICTED"
        assert result.json()["checks"]["quote_verified"] is True
        assert client.get("/api/reviews").status_code == 200

