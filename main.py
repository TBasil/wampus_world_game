import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
TILE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD_COLOR = (255, 215, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extended Wampus World")

# Fonts for displaying text
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)


# Define the Player, Wampus, Pit, and Gold classes
class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.arrow = True  # Player starts with one arrow
        self.has_gold = False

    def move(self, dx, dy):
        # Ensure the player doesn't move out of bounds
        new_row = self.row + dy
        new_col = self.col + dx
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            self.row = new_row
            self.col = new_col

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Wampus:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.alive = True

    def move_random(self):
        # Wampus moves randomly if alive
        if self.alive:
            direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])  # Right, Down, Left, Up
            new_row = self.row + direction[0]
            new_col = self.col + direction[1]
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                self.row = new_row
                self.col = new_col

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, RED, (self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Pit:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Gold:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            pygame.draw.rect(screen, GOLD_COLOR, (self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


# Setup initial game state
player = Player(0, 0)  # Player starts at the top-left corner
wampus = Wampus(random.randint(0, ROWS - 1), random.randint(0, COLS - 1))  # Wampus starts at a random position
pits = [Pit(random.randint(0, ROWS - 1), random.randint(0, COLS - 1)) for _ in range(5)]  # 5 random pits
gold = Gold(random.randint(0, ROWS - 1), random.randint(0, COLS - 1))  # Gold at a random position

# Game loop
running = True
clock = pygame.time.Clock()
wampus_move_timer = 0  # Timer to control Wampus movement speed
game_start = True  # Show start screen with controls

while running:
    screen.fill(WHITE)

    # Display game instructions on start screen
    if game_start:
        instructions = [
            "Welcome to the Extended Wampus World!",
            "Use arrow keys to move the player:",
            "- Up: Arrow Up",
            "- Down: Arrow Down",
            "- Left: Arrow Left",
            "- Right: Arrow Right",
            "Press 'Space' to shoot the arrow.",
            "Goal: Collect the gold, kill the Wampus, and return to the start to win!",
            "Press any key to begin!"
        ]
        for idx, line in enumerate(instructions):
            text = font.render(line, True, BLACK)
            screen.blit(text, (50, 50 + idx * 40))
        pygame.display.flip()

        # Wait for key press to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game_start = False  # Start the game after key press
        continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0)
    if keys[pygame.K_UP]:
        player.move(0, -1)
    if keys[pygame.K_DOWN]:
        player.move(0, 1)

    # Player shoots arrow
    if keys[pygame.K_SPACE] and player.arrow:
        if (player.row == wampus.row or player.col == wampus.col) and wampus.alive:
            wampus.alive = False  # Kill Wampus if on the same row or column
            print("You killed the Wampus!")
        player.arrow = False  # Player can only shoot once

    # Move Wampus periodically (every 1 second)
    wampus_move_timer += clock.get_time()
    if wampus_move_timer > 1000:  # Move every 1000 ms (1 second)
        wampus.move_random()
        wampus_move_timer = 0

    # Draw everything
    player.draw(screen)
    wampus.draw(screen)
    for pit in pits:
        pit.draw(screen)
    gold.draw(screen)

    # Check if player collects gold
    if player.row == gold.row and player.col == gold.col and not gold.collected:
        gold.collected = True
        player.has_gold = True
        print("You collected the gold!")

    # Check if player falls into a pit
    for pit in pits:
        if player.row == pit.row and player.col == pit.col:
            print("You fell into a pit!")
            running = False

    # Check if player returns to start after collecting gold
    if player.row == 0 and player.col == 0 and player.has_gold:
        print("You returned to the start with the gold! You win!")
        running = False

    # Check if player gets caught by Wampus
    if player.row == wampus.row and player.col == wampus.col and wampus.alive:
        print("You were caught by the Wampus!")
        running = False

    # Update display and tick clock
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()

