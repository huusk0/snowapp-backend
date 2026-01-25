import pygame
import sys
import math
import copy

pygame.init()

# Screen setup
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("test")

# lumikola settings
kola_width = 1
kola_height = 1
kola_capacity = 10

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


def main():
    clock = pygame.time.Clock()
    running = True

    screen.fill(DARK_GRAY)
    pygame.draw.rect(screen, BLUE, button_rect)
    text = font.render("split", True, WHITE)
    screen.blit(text, (button_rect.x + 25, button_rect.y + 10))
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
