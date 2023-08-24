import random
import pygame
import time

# Fensterdimensionen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Farben definieren
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Funktion zum Generieren des Labyrinths
def generate_maze(width, height):
    maze = [['#' for _ in range(width)] for _ in range(height)]
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            if random.random() < 0.7:
                maze[row][col] = ' '
    return maze

# Funktion für die Tiefensuche
def depth_first_search(maze, row, col):
    """
    Tiefensuche zum Finden des Ausgangs
    """
    ...
    raise NotImplementedError

def search_exit():
    """
    Anstoßen der Suche nach dem Ausgang und Feedback für den Player
    """
    found_exit = depth_first_search(maze, person_row, person_col)
    if found_exit:
        print("\nAusgang gefunden!")
    else:
        print("\nKein Ausgang gefunden!")

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Visualization")

# Generiere das Labyrinth
width, height = 15, 10
maze = generate_maze(width, height)
maze[1][0] = 'E'
maze[-2][-1] = 'A'
person_row, person_col = 1, 0

# Pygame Schleife für Bewegung und weitere Logik
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Schließe Pygame
            exit()  # Beende das Programm

        # Bewegung der Person mit den WASD-Tasten
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and maze[person_row - 1][person_col] == ' ':
                person_row -= 1
            elif event.key == pygame.K_s and maze[person_row + 1][person_col] == ' ':
                person_row += 1
            elif event.key == pygame.K_a and maze[person_row][person_col - 1] == ' ':
                person_col -= 1
            elif event.key == pygame.K_d and maze[person_row][person_col + 1] == ' ':
                person_col += 1

    screen.fill(BLACK)  # Lösche den vorherigen Frame

    # Zeichne das Labyrinth
    for row in range(height):
        for col in range(width):
            color = BLACK
            if maze[row][col] == ' ':
                color = WHITE
            elif maze[row][col] == 'E':
                color = GREEN
            elif maze[row][col] == 'A':
                color = RED

            pygame.draw.rect(screen, color, (col * 40, row * 40, 40, 40))

    # Zeichne die bewegliche Person
    pygame.draw.rect(screen, YELLOW, (person_col * 40, person_row * 40, 40, 40))

    pygame.display.flip()




