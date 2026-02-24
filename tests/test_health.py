def test_health_returns_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ok"


def test_health_has_timing_header(client):
    resp = client.get("/health")
    assert "X-Process-Time" in resp.headers
