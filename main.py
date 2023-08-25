"""
Suchstrategie vs Suchstrategie Player = Tiefensuche Monster = Breitensuche
Step 1: Der Spieler bekommt Hilfe durch die Darstellung des kürzesten Weges basierend auf der Tiefensuche - done
Step 2: Das Monster bewegt sich Random - done
Step 3: Bewegt sich der Spieler hört das Monster den Spieler und führt eine Breitensuche aus und geht einen Schritt - done
Step 4: Das Monster lernt zu sehen, ist ein grader, ununterbrochener Pfad vorhanden, schlägt das Monster den kürzesten Weg ein um den Spieler zu kriegen
Step 5: Der Spieler kann sich verstecken so dass das Monster ihn nicht mehr sehen und hören kann. - done
Step 5: Es gibt Level - done
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
PLAYER_HIDE = (255, 255, 255, 125)

# Pygame Schleife für Bewegung und weitere Logik
dragging = False
drag_start = None

# Initialisiere den Zähler für die Tiefe
depth_counter = 1

player_row, player_col = 0, 0

# Initialisiere die Position des Monsters in der Mitte des Labyrinths
monster_row = 0
monster_col = 0

# Exit Position
exit_row = 0
exit_col = 0


# Funktion zum Generieren des Labyrinths
def generate_maze(maze_width, maze_height, number_of_generated_mate_paths):
    global maze
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
    for i in range(number_of_generated_mate_paths):
        generate_maze_path(maze, maze_height, maze_width, random.randint(0, maze_height - 1),
                           random.randint(0, maze_width - 1), False)

    set_screen_offset()
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


def move_monster_random(monster_speed):
    global monster_row, monster_col

    for i in range(monster_speed):
        # Liste der möglichen Bewegungsrichtungen (oben, unten, links, rechts)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Zufällig eine Richtung auswählen
        random_direction = random.choice(directions)
        new_monster_row = monster_row + random_direction[0]
        new_monster_col = monster_col + random_direction[1]

        # Überprüfen, ob die neue Position gültig ist
        if 0 <= new_monster_row < maze_height and 0 <= new_monster_col < maze_width and maze[new_monster_row][
            new_monster_col] == ' ':
            # Monster an die neue Position bewegen
            monster_row = new_monster_row
            monster_col = new_monster_col


def move_monster_to_player_path(path_to_player, monster_speed):
    for i in range(monster_speed):
        if len(path_to_player) > 1:
            # Entferne das erste Element aus dem Pfad
            path_to_player.pop(0)

            # Nächste Position im Pfad
            next_row, next_col = path_to_player[0]

            global monster_row, monster_col
            monster_row = next_row
            monster_col = next_col


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
    FOUND_EXIT = 1
    GAME_OVER = 2


def trigger_event(event_type):
    if event_type == Event.FOUND_EXIT:
        exit_event()
    if event_type == Event.GAME_OVER:
        game_over_event()


def game_over_event():
    global depth_counter  # Zugriff auf die globale Variable
    screen.fill(BLACK)
    depth_counter = 1  # Zähler zurücksetzen
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
                    generate_maze(maze_width, maze_height, 10)
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
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif game_event.type == pygame.KEYDOWN:
                if game_event.key == pygame.K_SPACE:
                    generate_maze(maze_width, maze_height, 10)
                    waiting_for_input = False


# Funktion für die Breitensuche
def breadth_first_search(start_row, start_col, target_row, target_col):
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


def set_screen_offset():
    global x_offset, y_offset, player_col, player_row
    x_offset = SCREEN_WIDTH // 2 - player_col * 40
    y_offset = SCREEN_HEIGHT // 2 - player_row * 40


# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Visualization")

# Generiere das Labyrinth
maze_width, maze_height = 25, 25
maze = generate_maze(maze_width, maze_height, 10)
# maze[1][0] = 'E'
# maze[-2][-1] = 'A'
# player_row, player_col = 1, 0


# Berechne den Abstand, um das Labyrinth in der Mitte anzuzeigen
visual_width = maze_width * 40  # Breite des Labyrinths in Pixeln
visual_height = maze_height * 40  # Höhe des Labyrinths in Pixeln
x_offset = SCREEN_WIDTH // 2 - player_col * 40
y_offset = SCREEN_HEIGHT // 2 - player_row * 40

# Pygame Schleife für Bewegung und weitere Logik
while True:

    # In der Pygame-Schleife
    clock = pygame.time.Clock()
    key_repeat_delay = 200  # Zeit in Millisekunden
    last_key_event_time = 0

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

        player_hide = False
        player_moved = False
        current_time = pygame.time.get_ticks()

        if current_time - last_key_event_time > key_repeat_delay:
            # Bewegung des Spielers mit den WASD-Tasten
            keys = pygame.key.get_pressed()

            # Bewegung der Person mit den WASD-Tasten
            if keys[pygame.K_w] \
                    and player_row - 1 >= 0 \
                    and maze[player_row - 1][player_col] in [' ', 'A', 'E']:
                player_row -= 1
                player_moved = True
                last_key_event_time = current_time

            if keys[pygame.K_s] \
                    and player_row + 1 < maze_height \
                    and maze[player_row + 1][player_col] in [' ', 'A', 'E']:
                player_row += 1
                player_moved = True
                last_key_event_time = current_time

            if keys[pygame.K_a] \
                    and player_col - 1 >= 0 \
                    and maze[player_row][player_col - 1] in [' ', 'A', 'E']:
                player_col -= 1
                player_moved = True
                last_key_event_time = current_time

            if keys[pygame.K_d] \
                    and player_col + 1 < maze_width \
                    and maze[player_row][player_col + 1] in [' ', 'A', 'E']:
                player_col += 1
                player_moved = True
                last_key_event_time = current_time

            if keys[pygame.K_SPACE]:
                move_monster_random(depth_counter)
                player_hide = True
                player_moved = True
                last_key_event_time = current_time

            # Nachdem der Spieler sich bewegt hat, das Monster ebenfalls bewegen
            if not player_hide and player_moved:
                # Breitensuche durchführen
                path_to_player = breadth_first_search(monster_row, monster_col, player_row, player_col)
                if path_to_player:
                    move_monster_to_player_path(path_to_player, depth_counter)

            if maze[player_row][player_col] == 'A':
                trigger_event(Event.FOUND_EXIT)

            if player_row == monster_row and player_col == monster_col:
                trigger_event(Event.GAME_OVER)

            # Breitensuche durchführen
            path_to_exit = breadth_first_search(player_row, player_col, exit_row, exit_col)

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

                    # Verwende die berechneten Offset-Werte, um das Labyrinth zu positionieren
                    pygame.draw.rect(screen, color, (x_offset + col * 40, y_offset + row * 40, 40, 40))

            # Zeichne des Spielers mit den verschobenen Positionen
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

            clock.tick(60)  # Begrenze die Schleifenrate auf 60 FPS

            # Blitte das Pfad-Overlay auf den Bildschirm
            screen.blit(path_overlay, (x_offset, y_offset))

            pygame.display.flip()
