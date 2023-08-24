"""
Suchstrategie vs Suchstrategie Player = Tiefensuche Monster = Breitensuche
Step 1: Der Spieler bekommt Hilfe durch die Darstellung des kürzesten Weges basierend auf der Tiefensuche
Step 2: Das Monster bewegt sich Random
Step 3: Bewegt sich der Spieler hört das Monster den Spieler und führt eine Breitensuche aus und geht einen Schritt
Step 4: Das Monster lernt zu sehen, ist ein grader, ununterbrochener Pfad vorhanden, schlägt das Monster den kürzesten Weg ein um den Spieler zu kriegen
Step 5: Der Spieler kann sich verstecken so dass das Monster ihn nicht mehr sehen kann.
Step 5: Es gibt Level
Step 6: Pro Level kann sich das Monster ein Feld weiterbewegen



"""

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
    found_exit = depth_first_search(maze, player_row, player_col)
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
player_row, player_col = 1, 0

# Pygame Schleife für Bewegung und weitere Logik
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Schließe Pygame
            exit()  # Beende das Programm

        # Bewegung der Person mit den WASD-Tasten
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and maze[player_row - 1][player_col] == ' ':
                player_row -= 1
            elif event.key == pygame.K_s and maze[player_row + 1][player_col] == ' ':
                player_row += 1
            elif event.key == pygame.K_a and maze[player_row][player_col - 1] == ' ':
                player_col -= 1
            elif event.key == pygame.K_d and maze[player_row][player_col + 1] == ' ':
                player_col += 1

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
    pygame.draw.rect(screen, YELLOW, (player_col * 40, player_row * 40, 40, 40))

    pygame.display.flip()




