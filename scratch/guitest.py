import pygame
import sys
import math
import copy
from areatest import Area
from snowSector import SnowSector

pygame.init()

# Screen setup
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("test")

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

scale = 3
x_offset = 10
y_offset = 10

areas = [
    Area(40 * scale, 30 * scale, 10 * scale, (100 * scale, 10 * scale)),
    Area(60 * scale, 50 * scale, 10 * scale, (80 * scale, 50 * scale)),
    Area(40 * scale, 20 * scale, 10 * scale, (80 * scale, 110 * scale)),
    Area(20 * scale, 20 * scale, 10 * scale, (80 * scale, 150 * scale)),
    Area(20 * scale, 40 * scale, 10 * scale, (40 * scale, 150 * scale)),
    Area(10 * scale, 20 * scale, 10 * scale, (20 * scale, 160 * scale)),
    Area(30 * scale, 20 * scale, 10 * scale, (40 * scale, 170 * scale)),
]

snow_sectors = [SnowSector((10, 10), 100, "RED")]


def draw_areas():
    for area in areas:
        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
            (*area.coords, area.width, area.height),
        )


def draw_snow_sectors():
    for sector in snow_sectors:
        pygame.draw.circle(screen, sector.color, sector.coords, 1 * scale)


def split_to_sectors():
    for area in areas[0:2]:
        for i in range(0, math.ceil(area.width / kola_width)):
            for j in range(0, math.ceil(area.height / kola_height)):
                snow_sector = SnowSector(
                    (
                        area.coords[0] + x_offset * (i + 1),
                        area.coords[1] + y_offset * (j + 1),
                    ),
                    area.height * area.width * area.snow_depth,
                    "BLUE",
                )
                snow_sectors.append(snow_sector)


def main():
    clock = pygame.time.Clock()
    running = True

    screen.fill(DARK_GRAY)
    pygame.draw.rect(screen, BLUE, button_rect)
    text = font.render("split", True, WHITE)
    screen.blit(text, (button_rect.x + 25, button_rect.y + 10))
    split_to_sectors()
    draw_areas()
    draw_snow_sectors()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("hello from button")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print("Starting Disc Golf Simulator...")
    main()
