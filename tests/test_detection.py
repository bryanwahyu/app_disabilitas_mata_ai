from io import BytesIO


def test_detect_objects(client, sample_image_bytes):
    resp = client.post(
        "/api/v1/vision/detect",
        files={"file": ("test.jpg", BytesIO(sample_image_bytes), "image/jpeg")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["message"] == "Objek berhasil dideteksi"
    assert len(data["data"]["objects"]) == 2
    assert data["data"]["objects"][0]["name"] == "cat"


def test_detect_rejects_invalid_content_type(client):
    resp = client.post(
        "/api/v1/vision/detect",
        files={"file": ("test.txt", BytesIO(b"not an image"), "text/plain")},
    )
    assert resp.status_code == 400
