# import numpy as np
# scores = {
#   1: 10,
#   2: -10,
#   0: 0
# }
# player=1
# result = player if False else 0
# if result is not None:
#   print(scores[result])

# import numpy as np
import pygame

# Constants
WIDTH = 800
HEIGHT = 800
GRID_SIZE = 5
SCORE_AREA_HEIGHT = 100
SQUARE_SIZE = WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
# WHITE = (238,238,210)
# GRAY = (118,150,86)
# WHITE = "#e2e2e2"
# GRAY = "#00695C"


# GRAY = "#00695C"
# #aa9b83
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + SCORE_AREA_HEIGHT))
pygame.display.set_caption("Chessboard")

# Draw the chessboard
def draw_chessboard():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

# Draw the score area
def draw_score_area():
    pygame.draw.rect(screen, BLACK, (0, HEIGHT, WIDTH, SCORE_AREA_HEIGHT))

# Get the cell indices based on mouse position
def get_cell_indices(mouse_pos):
    x, y = mouse_pos
    row = y // SQUARE_SIZE  
    col = x // SQUARE_SIZE
    return row, col

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)  # Clear the screen
    draw_chessboard()   # Draw the chessboard
    draw_score_area()   # Draw the score area

    # Handle cell hover
    mouse_pos = pygame.mouse.get_pos()
    if HEIGHT > mouse_pos[1] >= 0:
        row, col = get_cell_indices(mouse_pos)
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        # if (row + col) % 2 == 0:
            # pygame.draw.rect(screen, YELLOW, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        # else:
        pygame.draw.rect(screen, GREEN, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    fonts = pygame.font.get_fonts()
    print(fonts)
    pygame.display.update()
    # clock.tick(50)

pygame.quit()
