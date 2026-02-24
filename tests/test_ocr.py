from io import BytesIO


def test_ocr_extract_text(client, sample_image_bytes):
    resp = client.post(
        "/api/v1/vision/ocr",
        files={"file": ("test.jpg", BytesIO(sample_image_bytes), "image/jpeg")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["message"] == "Teks berhasil dibaca"
    assert data["data"]["text"] == "Hello World"
    assert data["data"]["language"] == "ind+eng"
