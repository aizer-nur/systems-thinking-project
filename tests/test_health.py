# Switched to pytest fixture so I don't need to create TestClient in every test
# Keeps code cleaner

def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True, "degraded": False}