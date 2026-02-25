import math
from snowSector import SnowSector


class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


def split_to_sectors(
    areas: list[Rectangle], kola_width, kola_height
) -> list[SnowSector]:
    snow_sectors = []
    for area in areas:
        for i in range(0, math.floor(area.width / kola_width)):
            for j in range(0, math.floor(area.height / kola_height)):
                snow_sector = SnowSector(
                    (
                        area.coords[0] - kola_width // 2 + kola_width * (i + 1),
                        area.coords[1] - kola_height // 2 + kola_height * (j + 1),
                    ),
                    area.snow_depth,
                    "GREEN",
                )
                snow_sectors.append(snow_sector)
            if area.height - (j + 1) * kola_height > 0:
                snow_sector = SnowSector(
                    (
                        area.coords[0] - kola_width // 2 + kola_width * (i + 1),
                        area.coords[1] - kola_height // 2 + kola_height * (j + 2),
                    ),
                    area.snow_depth,
                    "RED",
                )
                snow_sectors.append(snow_sector)
        if area.width - (i + 1) * kola_width > 0:
            for j in range(0, math.floor(area.height / kola_height)):
                snow_sector = SnowSector(
                    (
                        area.coords[0] - kola_width // 2 + kola_width * (i + 2),
                        area.coords[1] - kola_height // 2 + kola_height * (j + 1),
                    ),
                    area.snow_depth,
                    "RED",
                )
                snow_sectors.append(snow_sector)
    return snow_sectors
