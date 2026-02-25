import pytest
from src.logic.rectModel import GeometryService, Rectangle


class TestEdgePoints:
    @pytest.fixture
    def geometry_service(self):
        return GeometryService()

    def test_calculating_edges_should_return_empty_on_None_input(
        self, geometry_service
    ):
        assert geometry_service.calculate_edge_points(None) == {}

    @pytest.mark.parametrize(
        "rectangle, expected",
        [
            (
                Rectangle(x=0, y=0, width=1, height=1),
                {"x1": 0, "y1": 0, "x2": 1, "y2": 1},
            ),
            (
                Rectangle(x=10, y=20, width=5, height=5),
                {"x1": 10, "y1": 20, "x2": 15, "y2": 25},
            ),
        ],
    )
    def test_calculating_edges_should_return_correct_edge_points(
        self, geometry_service, rectangle, expected
    ):
        expected_output = {
            "topleft": {"x": expected["x1"], "y": expected["y1"]},
            "topright": {"x": expected["x2"], "y": expected["y1"]},
            "bottomleft": {"x": expected["x1"], "y": expected["y2"]},
            "bottomright": {
                "x": expected["x2"],
                "y": expected["y2"],
            },
        }
        assert geometry_service.calculate_edge_points(rectangle) == expected_output

    def test_calculating_edges_should_return_edge_points_with_0_height(
        self, geometry_service
    ):
        rect = Rectangle(x=10, y=10, width=5, height=0)
        result = geometry_service.calculate_edge_points(rect)

        assert result["topleft"] == {"x": 10, "y": 10}
        assert result["bottomright"] == {"x": 15, "y": 10}

    def test_calculating_edges_should_return_edge_points_with_0_width(
        self, geometry_service
    ):
        rect = Rectangle(x=10, y=10, width=0, height=5)
        result = geometry_service.calculate_edge_points(rect)

        assert result["topleft"] == {"x": 10, "y": 10}
        assert result["bottomright"] == {"x": 10, "y": 15}
