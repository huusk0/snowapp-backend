from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestGreeting:
    def test_api_should_return_greeting(
        self,
    ):
        response = client.get("/api/greeting/")
        assert response.status_code == 200
        assert response.json() == {"text": "Hello world from API"}


class TestRectangleEdges:
    def test_modify_rects_with_valid_data_returns_200(self):
        response = client.post(
            "/api/rectangles/", json=[{"x": 0, "y": 0, "width": 1, "height": 1}]
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                "topleft": {"x": 0, "y": 0},
                "topright": {"x": 1, "y": 0},
                "bottomleft": {"x": 0, "y": 1},
                "bottomright": {"x": 1, "y": 1},
            }
        ]

    def test_modify_rects_with_negative_width_returns_422(self):
        response = client.post(
            "/api/rectangles/", json=[{"x": 0, "y": 0, "width": -1, "height": 1}]
        )
        assert response.status_code == 422

    def test_modify_rects_with_0_width_returns_422(self):
        response = client.post(
            "/api/rectangles/", json=[{"x": 0, "y": 0, "width": 0, "height": 1}]
        )
        assert response.status_code == 422

    def test_modify_rects_with_negative_height_returns_422(self):
        response = client.post(
            "/api/rectangles/", json=[{"x": 0, "y": 0, "width": 1, "height": -1}]
        )
        assert response.status_code == 422

    def test_modify_rects_with_0_height_returns_422(self):
        response = client.post(
            "/api/rectangles/", json=[{"x": 0, "y": 0, "width": 1, "height": 0}]
        )
        assert response.status_code == 422

    def test_modify_rects_with_missing_required_field_returns_422(self):
        response = client.post("/api/rectangles/", json=[{"x": 0, "y": 0, "width": 1}])
        assert response.status_code == 422
