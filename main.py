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
from enum import Enum

# Fensterdimensionen
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800

# Farben definieren
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Pygame Schleife für Bewegung und weitere Logik
dragging = False
drag_start = None

# Initialisiere den Zähler für die Tiefe
depth_counter = 0

# Funktion zum Generieren des Labyrinths
def generate_maze(maze_width, maze_height):
    maze = [['#' for _ in range(maze_width)] for _ in range(maze_height)]
    for row in range(1, maze_height - 1):
        for col in range(1, maze_width - 1):
            if random.random() < 0.9:
                maze[row][col] = ' '
    return maze


def generate_new_maze():
    global maze, player_row, player_col
    maze = generate_maze(width, height)
    maze[1][0] = 'E'
    maze[-2][-1] = 'A'
    player_row, player_col = 1, 0


# Funktion zum Anzeigen des Zählers über dem Labyrinth
def display_depth_counter(counter):
    font = pygame.font.Font(None, 30)
    text_surface = font.render(f"Tiefe: {counter}", True, WHITE)
    text_rect = text_surface.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
    screen.blit(text_surface, text_rect)

# Hinzufügen eines Monsters in der Mitte des Labyrinths
def draw_monster():
    monster_color = RED
    pygame.draw.rect(screen, monster_color, (x_offset + monster_col * 40, y_offset + monster_row * 40, 40, 40))

# Funktion zum Anzeigen von Text im Spiel
def display_message(messages, text_color):
    screen.fill(BLACK)  # Lösche den vorherigen Frame

    font = pygame.font.Font(None, 50)
    line_spacing = font.get_linesize()
    text_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    for message in messages:
        text_surface = font.render(message, True, text_color)
        text_rect = text_surface.get_rect(center=text_position)  # Erhalte das Rechteck der Textfläche
        screen.blit(text_surface, text_rect.topleft)  # Blit Text an die richtige Position
        text_position = (text_position[0], text_position[1] + line_spacing)  # Aktualisiere die Y-Position

    pygame.display.flip()


exit_messages = [
    "Ausgang gefunden!",
    "Du bewegst dich tiefer ins Labyrinth.",
    "Zum Fortsetzen drücke bitte die Leertaste."
]

game_over_messages = [
    "Du wurdest erwischt!",
    "Zum Neustarten drücke bitte die Leertaste."
]


class Event(Enum):
    FOUNDEXIT = 1
    GAMEOVER = 2


def trigger_event(event_type):
    if event_type == Event.FOUNDEXIT:
        exit_event()
    if event_type == Event.GAMEOVER:
        game_over_event()


def game_over_event():
    global depth_counter  # Zugriff auf die globale Variable
    screen.fill(BLACK)
    depth_counter = 0  # Zähler zurücksetzen
    display_message(game_over_messages, RED)
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generate_new_maze()
                    waiting_for_input = False


def exit_event():
    global depth_counter  # Zugriff auf die globale Variable
    maze[-2][-1] = ' '  # Das Ausgangsfeld leer machen
    display_message(exit_messages, WHITE)
    depth_counter += 1  # Zähler erhöhen
    display_depth_counter(depth_counter)  # Zähler anzeigen
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generate_new_maze()
                    waiting_for_input = False


# Funktion für die Tiefensuche
def depth_first_search(maze, row, col):
    """
    Tiefensuche zum Finden des Ausgangs
    """
    ...
    raise NotImplementedError


# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Visualization")

# Generiere das Labyrinth
width, height = 20, 15
maze = generate_maze(width, height)
maze[1][0] = 'E'
maze[-2][-1] = 'A'
player_row, player_col = 1, 0

# Initialisiere die Position des Monsters in der Mitte des Labyrinths
monster_row = len(maze) // 2
monster_col = len(maze[0]) // 2

# Berechne den Abstand, um das Labyrinth in der Mitte anzuzeigen
maze_width = width * 40  # Breite des Labyrinths in Pixeln
maze_height = height * 40  # Höhe des Labyrinths in Pixeln
x_offset = (SCREEN_WIDTH - maze_width) // 2
y_offset = (SCREEN_HEIGHT - maze_height) // 2

# Pygame Schleife für Bewegung und weitere Logik
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Rechte Maustaste gedrückt
            dragging = True
            drag_start = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:  # Rechte Maustaste losgelassen
            dragging = False

        if dragging:
            # Berechne die Verschiebung
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - drag_start[0]
            dy = mouse_y - drag_start[1]
            x_offset += dx
            y_offset += dy
            drag_start = (mouse_x, mouse_y)

        # Bewegung der Person mit den WASD-Tasten
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and maze[player_row - 1][player_col] in [' ', 'A']:
                player_row -= 1
            elif event.key == pygame.K_s and maze[player_row + 1][player_col] in [' ', 'A']:
                player_row += 1
            elif event.key == pygame.K_a and maze[player_row][player_col - 1] in [' ', 'A']:
                player_col -= 1
            elif event.key == pygame.K_d and maze[player_row][player_col + 1] in [' ', 'A']:
                player_col += 1
            if maze[player_row][player_col] == 'A':
                trigger_event(Event.FOUNDEXIT)

        if player_row == monster_row and player_col == monster_col:
            trigger_event(Event.GAMEOVER)

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
                color = BLUE

            # Verwende die berechneten Offset-Werte, um das Labyrinth zu zentrieren
            pygame.draw.rect(screen, color, (x_offset + col * 40, y_offset + row * 40, 40, 40))

    # Zeichne die bewegliche Person mit den verschobenen Positionen
    pygame.draw.rect(screen, YELLOW, (x_offset + player_col * 40, y_offset + player_row * 40, 40, 40))

    # Zeige den Zähler über dem Labyrinth an
    display_depth_counter(depth_counter)

    # Einfügen des Monsters
    draw_monster()

    pygame.display.flip()
