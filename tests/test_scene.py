from io import BytesIO


def test_describe_scene(client, sample_image_bytes):
    resp = client.post(
        "/api/v1/vision/describe",
        files={"file": ("test.jpg", BytesIO(sample_image_bytes), "image/jpeg")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["message"] == "Scene berhasil dideskripsikan"
    assert "caption" in data["data"]
    assert "detail" in data["data"]
    assert "caption_id" in data["data"]
    assert "detail_id" in data["data"]
