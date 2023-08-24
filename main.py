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
SHORTEST_PATH_COLOUR = (0, 255, 0, 50)

# Pygame Schleife für Bewegung und weitere Logik
dragging = False
drag_start = None

# Initialisiere den Zähler für die Tiefe
depth_counter = 0

player_row, player_col = 0, 0

# Initialisiere die Position des Monsters in der Mitte des Labyrinths
monster_row = 0
monster_col = 0

# Exit Position
exit_row = 0
exit_col = 0


# Funktion zum Generieren des Labyrinths
def generate_maze(maze_width, maze_height):
    # Maze mit # befüllen # = Wände
    maze = [['#' for _ in range(maze_width)] for _ in range(maze_height)]

    # Random Starting Position
    start_x = random.randint(0, maze_height - 1)
    start_y = random.randint(0, maze_width - 1)

    # Player Start Position
    maze[start_x][start_y] = 'E'

    # Tracking der Player Position setzen (Es soll nicht nach jeder Bewegung das ganze Array durchsucht werden
    global player_row, player_col
    player_row, player_col = start_x, start_y

    # Pfad von der Startposition zum Ausgang generieren
    wall_x, wall_y = generate_maze_path(maze, maze_height, maze_width, start_x, start_y, True)

    maze[wall_x][wall_y] = 'A'
    global exit_col, exit_row
    exit_row = wall_x
    exit_col = wall_y

    # Weitere Pfade generieren
    generate_maze_path(maze, maze_height, maze_width, random.randint(0, maze_height - 1),
                       random.randint(0, maze_width - 1), False)
    generate_maze_path(maze, maze_height, maze_width, random.randint(0, maze_height - 1),
                       random.randint(0, maze_width - 1), False)
    generate_maze_path(maze, maze_height, maze_width, random.randint(0, maze_height - 1),
                       random.randint(0, maze_width - 1), False)
    generate_maze_path(maze, maze_height, maze_width, random.randint(0, maze_height - 1),
                       random.randint(0, maze_width - 1), False)

    return maze


def generate_maze_path(maze, maze_width, maze_height, start_x, start_y, place_monster):
    walls = [(start_x, start_y)]
    wall_x, wall_y = 0, 0
    # Anlegen des Pfades zum Ausgang
    while walls:
        wall_x, wall_y = walls.pop(random.randint(0, len(walls) - 1))
        adjacent_cells = []

        if wall_x > 1:
            adjacent_cells.append((wall_x - 2, wall_y))
        if wall_x < maze_width - 2:
            adjacent_cells.append((wall_x + 2, wall_y))
        if wall_y > 1:
            adjacent_cells.append((wall_x, wall_y - 2))
        if wall_y < maze_height - 2:
            adjacent_cells.append((wall_x, wall_y + 2))

        random.shuffle(adjacent_cells)

        for adj_x, adj_y in adjacent_cells:
            if 0 <= adj_x < maze_height and 0 <= adj_y < maze_width and maze[adj_x][adj_y] == '#':
                maze[adj_x][adj_y] = ' '
                maze[wall_x + (adj_x - wall_x) // 2][wall_y + (adj_y - wall_y) // 2] = ' '
                walls.append((adj_x, adj_y))
                break

            # Monster in der Mitte des Pfades zwischen Ein- und Ausgang positionieren
            if place_monster:
                half_length_of_path = len(adjacent_cells) // 2
                middle_position = adjacent_cells[half_length_of_path]
                global monster_row, monster_col
                monster_row = middle_position[0]
                monster_col = middle_position[1]


    # Rückgabe des Ende des Pfades (Position des Ausgangs)
    return wall_x, wall_y


def generate_new_maze():
    global maze, player_row, player_col
    maze = generate_maze(maze_width, maze_height)
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
                    generate_maze(maze_width, maze_height)
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
                    generate_maze(maze_width, maze_height)
                    waiting_for_input = False


# Funktion für die Breitensuche
def breadth_first_search(maze, start_row, start_col, target_row, target_col):
    queue = [(start_row, start_col, [])]
    visited = set()

    while queue:
        current_row, current_col, path = queue.pop(0)
        if (current_row, current_col) in visited:
            continue
        visited.add((current_row, current_col))

        if current_row == target_row and current_col == target_col:
            return path

        neighbors = [
            (current_row - 1, current_col),
            (current_row + 1, current_col),
            (current_row, current_col - 1),
            (current_row, current_col + 1)
        ]

        for neighbor_row, neighbor_col in neighbors:
            if 0 <= neighbor_row < maze_height and 0 <= neighbor_col < maze_width:
                cell = maze[neighbor_row][neighbor_col]
                if cell in [' ', 'A']:
                    queue.append((neighbor_row, neighbor_col, path + [(current_row, current_col)]))

    return path


# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Visualization")

# Generiere das Labyrinth
maze_width, maze_height = 20, 15
maze = generate_maze(maze_width, maze_height)
# maze[1][0] = 'E'
# maze[-2][-1] = 'A'
# player_row, player_col = 1, 0


# Berechne den Abstand, um das Labyrinth in der Mitte anzuzeigen
visual_width = maze_width * 40  # Breite des Labyrinths in Pixeln
visual_height = maze_height * 40  # Höhe des Labyrinths in Pixeln
x_offset = (SCREEN_WIDTH - visual_width) // 2
y_offset = (SCREEN_HEIGHT - visual_height) // 2

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

            if event.key == pygame.K_w \
                    and player_row - 1 >= 0 \
                    and maze[player_row - 1][player_col] in [' ', 'A', 'E']:
                player_row -= 1

            elif event.key == pygame.K_s \
                    and player_row + 1 < maze_height \
                    and maze[player_row + 1][player_col] in [' ', 'A', 'E']:
                player_row += 1

            elif event.key == pygame.K_a \
                    and player_col - 1 >= 0 \
                    and maze[player_row][player_col - 1] in [' ', 'A', 'E']:
                player_col -= 1

            elif event.key == pygame.K_d \
                    and player_col + 1 < maze_width \
                    and maze[player_row][player_col + 1] in [' ', 'A', 'E']:
                player_col += 1

            if maze[player_row][player_col] == 'A':
                trigger_event(Event.FOUNDEXIT)

            if player_row == monster_row and player_col == monster_col:
                trigger_event(Event.GAMEOVER)

    # Breitensuche durchführen
    path_to_exit = breadth_first_search(maze, player_row, player_col, exit_row, exit_col)

    screen.fill(BLACK)  # Lösche den vorherigen Frame

    # Zeichne das Labyrinth
    for row in range(maze_height):
        for col in range(maze_width):
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

    # Erstelle ein Surface für den Pfad-Overlay
    path_overlay = pygame.Surface((visual_width, visual_height), pygame.SRCALPHA)
    if path_to_exit:
        for path_row, path_col in path_to_exit:
            if (path_row, path_col) != (player_row, player_col):
                pygame.draw.rect(path_overlay, SHORTEST_PATH_COLOUR, (path_col * 40, path_row * 40, 40, 40))

    # Blitte das Pfad-Overlay auf den Bildschirm
    screen.blit(path_overlay, (x_offset, y_offset))

    pygame.display.flip()
