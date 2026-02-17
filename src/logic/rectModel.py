from collections import defaultdict
import math
import networkx as nx


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

    def snow_sectors_to_coords(
        self, snow_sectors: list[SnowSector]
    ) -> list[tuple[int, int]]:
        coords = []
        for sector in snow_sectors:
            coords.append((sector.coords[0], sector.coords[1]))
        return coords

    def generate_edges(
        self,
        snow_sectors: list[SnowSector],
        kola_width: int = 10,
        kola_height: int = 10,
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        cols = defaultdict(list)
        rows = defaultdict(list)

        for sector in snow_sectors:
            x = sector.coords[0]
            y = sector.coords[1]
            cols[x].append(y)
            rows[y].append(x)

        for x in cols:
            cols[x].sort()  # sort y's in the same column
        for y in rows:
            rows[y].sort()  # sort x's in the same row

        edges = []

        # Connect along columns
        for x, y_list in cols.items():
            for i in range(len(y_list) - 1):
                if y_list[i + 1] - y_list[i] <= kola_width:
                    edges.append(((x, y_list[i]), (x, y_list[i + 1])))

        # Connect along rows
        for y, x_list in rows.items():
            for i in range(len(x_list) - 1):
                if x_list[i + 1] - x_list[i] <= kola_height:
                    edges.append(((x_list[i], y), (x_list[i + 1], y)))
        return edges

    def find_path_v0(
        self,
        areas: list[Rectangle],
        start_node: tuple[int, int] | None = None,
        kola_width: int = 10,
        kola_height: int = 10,
    ) -> list[tuple[int, int]]:
        snow_sectors = self.split_to_sectors(areas)
        coords = self.snow_sectors_to_coords(snow_sectors)
        edges = self.generate_edges(snow_sectors)
        G = nx.Graph()
        G.add_nodes_from(coords)
        G.add_edges_from(edges)
        tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)
        if start_node is None:
            start_node = coords[0]
        if start_node in tsp_path:
            idx = tsp_path.index(start_node)
            tsp_path = tsp_path[idx:] + tsp_path[:idx]

        return tsp_path
