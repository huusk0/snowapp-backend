import pygame
import sys
import math
import copy
from areatest import Area
from snowSector import SnowSector
from testAreaMaps import areas_1, areas_2, areas_basic, areas_overlay
from collections import defaultdict
import networkx as nx
from functions import split_to_sectors

pygame.init()

# Screen setup
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("test")

scale = 3

# lumikola settings
kola_width = 10
kola_height = 10
kola_capacity = 100

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
# Fonts
font = pygame.font.SysFont(None, 24)
# Button setup
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 60, 100, 40)
prev_pos = []
show_sectors = True

areas = areas_1
# areas = areas_2
# areas = areas_basic
# areas = areas_overlay

snow_sectors = []


def draw_areas():
    for area in areas:
        pygame.draw.rect(
            screen,
            WHITE,
            (
                area.coords[0] * scale,
                area.coords[1] * scale,
                area.width * scale,
                area.height * scale,
            ),
        )


def draw_snow_sectors():
    for sector in snow_sectors:
        pygame.draw.circle(
            screen,
            sector.color,
            (
                sector.coords[0] * scale,
                sector.coords[1] * scale,
            ),
            scale,
        )


def draw_lines():
    for i in range(0, len(snow_sectors) - 1):
        pygame.draw.line(
            screen,
            WHITE,
            (snow_sectors[i].coords[0] * scale, snow_sectors[i].coords[1] * scale),
            (
                snow_sectors[i + 1].coords[0] * scale,
                snow_sectors[i + 1].coords[1] * scale,
            ),
        )


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def sort_by_nearest(sectors, start=None):
    if not sectors:
        return []

    remaining = sectors[:]

    # Choose starting point
    if start is None:
        current = remaining.pop(0)
    else:
        current = min(remaining, key=lambda s: distance(s.coords, start))
        remaining.remove(current)

    ordered = [current]

    while remaining:
        next_sector = min(remaining, key=lambda s: distance(s.coords, current.coords))
        remaining.remove(next_sector)
        ordered.append(next_sector)
        current = next_sector

    return ordered


def draw_edges(edges_list):
    for edge in edges_list:
        pygame.draw.line(
            screen,
            BLACK,
            (edge[0][0] * scale, edge[0][1] * scale),
            (edge[1][0] * scale, edge[1][1] * scale),
        )


def draw_tsp(tsp_list):
    n = len(tsp_list)
    for i in range(0, n - 1):
        color_value = int((i / (n - 1)) * 255)
        color = (255 - color_value, 0, color_value)
        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
            (
                (tsp_list[i][0] - kola_width // 2) * scale,
                (tsp_list[i][1] - kola_height // 2) * scale,
                kola_width * scale,
                kola_height * scale,
            ),
        )
        pygame.draw.line(
            screen,
            color,
            (tsp_list[i][0] * scale, tsp_list[i][1] * scale),
            (tsp_list[i + 1][0] * scale, tsp_list[i + 1][1] * scale),
            width=3,
        )


def animate_path(tick, path, tsp_path_walked):
    pygame.draw.circle(screen, BLACK, (path[tick][0] * scale, path[tick][1] * scale), 5)
    tsp_path_walked.append(path[tick])


def generate_edges():
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


def snow_sectors_to_coords():
    coords = []
    for sector in snow_sectors:
        coords.append((sector.coords[0], sector.coords[1]))
    print("COORDS: ", coords)
    return coords


def find_path_v1(edges):
    G = nx.Graph()
    coords = snow_sectors_to_coords()
    G.add_nodes_from(coords)
    G.add_edges_from(edges)
    tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)
    start_node = coords[0]
    if start_node in tsp_path:
        idx = tsp_path.index(start_node)
        tsp_path = tsp_path[idx:] + tsp_path[:idx]

    return tsp_path


def main():
    global snow_sectors
    clock = pygame.time.Clock()
    running = True
    animate = False
    tick = 0
    snow_sectors = split_to_sectors(areas, kola_width, kola_height)
    edges = generate_edges()
    tsp_path = find_path_v1(edges)
    animation_length = len(tsp_path)
    tsp_path_walked = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    animate = True
                    tick = 0
                    tsp_path_walked = []

        screen.fill(DARK_GRAY)
        pygame.draw.rect(screen, BLUE, button_rect)
        text = font.render("animate", True, WHITE)
        screen.blit(text, (button_rect.x + 25, button_rect.y + 10))
        draw_areas()
        draw_snow_sectors()
        # draw_lines()
        # draw_edges(edges)
        # draw_tsp(tsp_path)
        draw_tsp(tsp_path_walked)
        if animate:
            animate_path(tick, tsp_path, tsp_path_walked)
            tick += 1

        if tick == animation_length:
            animate = False
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print("Simulator...")
    main()
