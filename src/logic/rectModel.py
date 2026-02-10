import math


class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class SnowSector:
    def __init__(self, coords, snow_load=None, color="yellow", dump_site=False):
        self.coords = coords
        self.snow_load = snow_load
        self.color = color
        self.dump_site = dump_site

    def __repr__(self):
        return f"Snow sector at: {self.coords}"


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

    def split_to_sectors(
        self,
        areas: list[Rectangle],
        kola_width: int = 10,
        kola_height: int = 10,
    ) -> list[SnowSector]:
        snow_sectors: list[SnowSector] = []

        for area in areas:
            full_x = area.width // kola_width
            full_y = area.height // kola_height

            for i in range(full_x):
                for j in range(full_y):
                    snow_sectors.append(
                        SnowSector(
                            coords=(
                                area.x + kola_width * i + kola_width // 2,
                                area.y + kola_height * j + kola_height // 2,
                            ),
                            snow_load=10,
                            color="GREEN",
                            dump_site=False,
                        )
                    )

                # remaining height strip
                if area.height % kola_height > 0:
                    snow_sectors.append(
                        SnowSector(
                            coords=(
                                area.x + kola_width * i + kola_width // 2,
                                area.y + kola_height * full_y + kola_height // 2,
                            ),
                            snow_load=10,
                            color="RED",
                            dump_site=True,
                        )
                    )

            # remaining width strip
            if area.width % kola_width > 0:
                for j in range(full_y):
                    snow_sectors.append(
                        SnowSector(
                            coords=(
                                area.x + kola_width * full_x + kola_width // 2,
                                area.y + kola_height * j + kola_height // 2,
                            ),
                            snow_load=10,
                            color="RED",
                            dump_site=True,
                        )
                    )

        return snow_sectors
