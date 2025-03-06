import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TAN = (245, 222, 179)
RED = (255, 0, 0)

# Load dice images
dice_images = [pygame.image.load(f"dice{i}.png") for i in range(1, 7)]
dice_images = [pygame.transform.scale(img, (50, 50)) for img in dice_images]

# Load player tokens
player1_img = pygame.image.load("player1.png")
player1_img = pygame.transform.scale(player1_img, (40, 40))
player2_img = pygame.image.load("player2.png")
player2_img = pygame.transform.scale(player2_img, (40, 40))

# Snakes
psnake = pygame.image.load("psnake.png")
psnake = pygame.transform.scale(psnake, (60, 180))
bsnake = pygame.image.load("bsnake.png")
bsnake = pygame.transform.scale(bsnake, (90, 150))
gsnake = pygame.image.load("gsnake.png")
gsnake = pygame.transform.scale(gsnake, (70, 120))

# Ladders
ladder = pygame.image.load("ladder.png")
ladder = pygame.transform.scale(ladder, (80, 120))

# Define Snakes & Ladders
snakes = {96: 65, 82: 57, 53: 33, 36: 5}
ladders = {19: 39, 29: 49, 62: 82, 73: 93}

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
pygame.display.set_caption("Snakes and Ladders")

# Dice Position
dice_x, dice_y = 250, 620
current_dice = 0

# Player Positions
player_positions = [1, 1]  
turn = 0  
winner = None  # Track if there's a winner

def draw_board():
    """Draws the board with the correct zig-zag numbering."""
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * SQUARE_SIZE, row * SQUARE_SIZE
            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, TAN if (row + col) % 2 == 0 else WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            # Calculate tile number based on zig-zag pattern
            tile_num = (ROWS - 1 - row) * 10  
            if (ROWS - 1 - row) % 2 == 0:  
                tile_num += col + 1
            else:  
                tile_num += (COLS - col)

            # Draw tile number
            font = pygame.font.Font(None, 20)
            text = font.render(str(tile_num), True, BLACK)
            screen.blit(text, (x + 20, y + 20))

    # Draw Snakes
    screen.blit(psnake, (230, 380))  # Example positions
    screen.blit(bsnake, (100, 160))
    screen.blit(gsnake, (420, 280))
    screen.blit(psnake, (250, 20))
    
    # Draw Ladders
    screen.blit(ladder, (55, 385))
    screen.blit(ladder, (47,85))
    screen.blit(ladder, (412, 35))
    screen.blit(ladder, (465, 340)) 

def get_tile_position(tile):
    """Converts a tile number into (x, y) pixel position following the zig-zag pattern correctly."""
    row = (tile - 1) // 10  
    col = (tile - 1) % 10  

    if row % 2 == 0:  
        x = col * SQUARE_SIZE + 10  
    else:  
        x = (9 - col) * SQUARE_SIZE + 10  

    y = (9 - row) * SQUARE_SIZE + 10  
    return x, y

def draw_players():
    """Draws players at their correct positions."""
    for i, pos in enumerate(player_positions):
        x, y = get_tile_position(pos)
        screen.blit(player1_img if i == 0 else player2_img, (x, y))

def roll_dice():
    """Rolls the dice and moves the player correctly."""
    global current_dice, turn, winner

    if winner is not None:
        return  # Stop rolling if the game is over

    dice_roll = random.randint(1, 6)
    current_dice = dice_roll - 1  

    new_pos = player_positions[turn] + dice_roll  

    if new_pos <= 100:  
        player_positions[turn] = new_pos  

        # Apply Snakes and Ladders
        if new_pos in snakes:
            player_positions[turn] = snakes[new_pos]
        elif new_pos in ladders:
            player_positions[turn] = ladders[new_pos]

    # Check for Win Condition
    if player_positions[turn] == 100:
        winner = turn  # Store the winner's index
        return  # Stop further moves

    # Switch Turn only after the current player finishes their move
    turn = 1 - turn  

def display_winner():
    """Displays the winning message."""
    font = pygame.font.Font(None, 50)
    text = font.render(f"🎉 Player {winner + 1} Wins! 🎉", True, RED)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 25))

def main():
    """Main game loop."""
    running = True
    
    while running:
        screen.fill(WHITE)
        draw_board()
        draw_players()
        screen.blit(dice_images[current_dice], (dice_x, dice_y))

        if winner is not None:
            display_winner()  # Show the winner

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                x, y = pygame.mouse.get_pos()
                if dice_x <= x <= dice_x + 50 and dice_y <= y <= dice_y + 50:
                    roll_dice()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
