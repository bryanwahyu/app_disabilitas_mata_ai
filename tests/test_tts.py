def test_tts_returns_audio(client):
    resp = client.post("/api/v1/vision/tts", json={"text": "Halo dunia"})
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "audio/mpeg"
    assert len(resp.content) > 0


def test_tts_rejects_empty_text(client, mock_tts_service):
    from app.domain.tts.service import TTSService

    mock_tts_service.speak.side_effect = ValueError("Teks tidak boleh kosong")
    resp = client.post("/api/v1/vision/tts", json={"text": "   "})
    assert resp.status_code == 400
