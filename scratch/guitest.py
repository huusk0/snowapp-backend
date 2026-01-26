import pygame
import sys
import math
import copy
from areatest import Area
from snowSector import SnowSector
from testAreaMaps import areas_1, areas_2, areas_basic

from collections import defaultdict

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

areas = areas_2

snow_sectors = []


def draw_areas():
    for area in areas:
        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
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


def split_to_sectors():
    for area in areas:
        for i in range(0, math.floor(area.width / kola_width)):
            for j in range(0, math.floor(area.height / kola_height)):
                snow_sector = SnowSector(
                    (
                        area.coords[0] - kola_width // 2 + kola_width * (i + 1),
                        area.coords[1] - kola_height // 2 + kola_height * (j + 1),
                    ),
                    area.height * area.width * area.snow_depth,
                    "GREEN",
                )
                snow_sectors.append(snow_sector)
            if area.height - (j + 1) * kola_height > 0:
                snow_sector = SnowSector(
                    (
                        area.coords[0] - kola_width // 2 + kola_width * (i + 1),
                        area.coords[1] - kola_height // 2 + kola_height * (j + 2),
                    ),
                    area.height * area.width * area.snow_depth,
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
                    area.height * area.width * area.snow_depth,
                    "RED",
                )
                snow_sectors.append(snow_sector)


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


def main():
    global snow_sectors
    clock = pygame.time.Clock()
    running = True

    split_to_sectors()
    edges = generate_edges()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    snow_sectors = sort_by_nearest(snow_sectors)

        screen.fill(DARK_GRAY)
        pygame.draw.rect(screen, BLUE, button_rect)
        text = font.render("split", True, WHITE)
        screen.blit(text, (button_rect.x + 25, button_rect.y + 10))
        draw_areas()
        draw_snow_sectors()
        # draw_lines()
        draw_edges(edges)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print("Starting Disc Golf Simulator...")
    main()
