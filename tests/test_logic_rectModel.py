import pytest
from src.logic.rectModel import GeometryService


@pytest.fixture
def geometry_service():
    return GeometryService()


def test_zero_input(geometry_service):
    rects = []
    assert geometry_service.calculate_edge_points(rects) == []
