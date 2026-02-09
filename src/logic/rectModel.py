class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class GeometryService:
    def calculate_edge_points(self, rectangle: Rectangle):
        return {
            "topleft": {"x": rectangle.x, "y": rectangle.y},
            "topright": {"x": rectangle.x + rectangle.width, "y": rectangle.y},
            "bottomleft": {"x": rectangle.x, "y": rectangle.y + rectangle.height},
            "bottomright": {
                "x": rectangle.x + rectangle.width,
                "y": rectangle.y + rectangle.height,
            },
        }
