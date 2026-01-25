import pygame
import sys
import math
import copy
from areatest import Area
from snowSector import SnowSector
from testAreaMaps import areas_1

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

snow_sectors = [SnowSector((10, 10), 100, "RED")]


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


def main():
    global show_sectors
    clock = pygame.time.Clock()
    running = True

    split_to_sectors()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    show_sectors = not show_sectors
                    print("show:", show_sectors)

        screen.fill(DARK_GRAY)
        pygame.draw.rect(screen, BLUE, button_rect)
        text = font.render("split", True, WHITE)
        screen.blit(text, (button_rect.x + 25, button_rect.y + 10))
        draw_areas()
        if show_sectors:
            draw_snow_sectors()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print("Starting Disc Golf Simulator...")
    main()
