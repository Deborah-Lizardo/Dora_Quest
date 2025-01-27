import pygame
import random

pygame.init()
pygame.display.set_caption("Dora, the Adventurous Snake")

# Create the clock (parameter that determines Dora's speed)
clock = pygame.time.Clock()

# Define game screen dimensions
WIDTH = 1000
HEIGHT = 600

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

# Define colors used in the game (RGB)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
LIGHT_PINK = (255, 102, 204)
DARK_PINK2 = (255, 51, 153)
DARK_PINK1 = (199, 21, 133)
LILAC = (204, 102, 255)
DORA_INITIAL_COLOR = (255, 153, 204)

# Dora's parameters
SQUARE_SIZE = 20
INITIAL_SPEED = 7

# Function to display the initial message explaining the game rules and welcoming the player
def show_initial_message():
    DISPLAY.fill(WHITE)
    font = pygame.font.SysFont("Arial", 24)
    title = font.render("Welcome to Dora, the Adventurous Snake!", True, DARK_PINK1)
    rule1 = font.render("Use the arrow keys to move Dora and collect 25 lilac backpacks!", True, DARK_PINK1)
    rule2 = font.render("Avoid the orange backpacks from Swiper; they reduce your score!", True, DARK_PINK1)
    rule3 = font.render("Let the adventure begin!", True, DARK_PINK1)

    DISPLAY.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 70))
    DISPLAY.blit(rule1, (WIDTH // 2 - rule1.get_width() // 2, HEIGHT // 2 - 30))
    DISPLAY.blit(rule2, (WIDTH // 2 - rule2.get_width() // 2, HEIGHT // 2 + 10))
    DISPLAY.blit(rule3, (WIDTH // 2 - rule3.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

# Function to generate lilac backpack
def generate_backpacks():
    backpack_x1 = round(random.randrange(0, WIDTH - SQUARE_SIZE) / SQUARE_SIZE) * SQUARE_SIZE
    backpack_y1 = round(random.randrange(0, HEIGHT - SQUARE_SIZE) / SQUARE_SIZE) * SQUARE_SIZE
    return backpack_x1, backpack_y1

# Function to draw lilac backpack
def draw_backpack1(backpack_size, backpack_x1, backpack_y1):
    pygame.draw.rect(DISPLAY, LILAC, [backpack_x1, backpack_y1, backpack_size, backpack_size])

# Function to generate orange backpack
def generate_orange_backpack():
    orange_x = round(random.randrange(0, WIDTH - SQUARE_SIZE) / SQUARE_SIZE) * SQUARE_SIZE
    orange_y = round(random.randrange(0, HEIGHT - SQUARE_SIZE) / SQUARE_SIZE) * SQUARE_SIZE
    return orange_x, orange_y

# Function to draw orange backpack
def draw_orange_backpack(backpack_size, orange_x, orange_y):
    pygame.draw.rect(DISPLAY, ORANGE, [orange_x, orange_y, backpack_size, backpack_size])

# Function to draw Dora
def draw_dora(square_size, pixels):
    for pixel in pixels:
        pygame.draw.rect(DISPLAY, DORA_INITIAL_COLOR, [pixel[0], pixel[1], square_size, square_size])

# Function to select speed based on key pressed, ensuring no opposite direction
def select_speed(key, current_speed):
    x_speed, y_speed = current_speed

    if key == pygame.K_DOWN and y_speed == 0:
        return 0, SQUARE_SIZE
    elif key == pygame.K_UP and y_speed == 0:
        return 0, -SQUARE_SIZE
    elif key == pygame.K_RIGHT and x_speed == 0:
        return SQUARE_SIZE, 0
    elif key == pygame.K_LEFT and x_speed == 0:
        return -SQUARE_SIZE, 0

    return x_speed, y_speed

# Function to draw the score
def draw_score(score):
    if score <= 0:
        font = pygame.font.SysFont("Arial", 20)
        text_over = font.render("You ran out of points! Adventure over!", True, DARK_PINK1)
        DISPLAY.blit(text_over, [(WIDTH - text_over.get_width()) // 2, (HEIGHT - text_over.get_height()) // 2])
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        exit()
    else:
        font = pygame.font.SysFont("Arial", 17)
        text = font.render(f"Score: {score}", True, DARK_PINK1)
        DISPLAY.blit(text, [3, 3])

# Main game loop
def run_game():
    game_over = False
    show_initial_message()
    pygame.time.delay(3000)

    # Dora's initial position and speed
    x = WIDTH / 2
    y = HEIGHT / 2
    x_speed = 0
    y_speed = 0

    pixels = []
    dora_size = 1
    speed = INITIAL_SPEED

    backpack_x, backpack_y = generate_backpacks()
    orange_backpack_x, orange_backpack_y = generate_orange_backpack()

    while not game_over:
        DISPLAY.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                x_speed, y_speed = select_speed(event.key, (x_speed, y_speed))

        x += x_speed
        y += y_speed

        # Check collision with walls
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_over = True
            font = pygame.font.SysFont("Arial", 50)
            text = font.render("Game Over! You hit the wall!", True, DARK_PINK1)
            DISPLAY.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)

        # Check collision with lilac backpack
        if x == backpack_x and y == backpack_y:
            dora_size += 1
            speed += 0.5  # Gradually increase speed
            if dora_size >= 26:
                game_over = True
                font = pygame.font.SysFont("Arial", 20)
                text = font.render("Congratulations! You won!", True, DARK_PINK1)
                DISPLAY.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(3000)
            backpack_x, backpack_y = generate_backpacks()

        # Check collision with orange backpack
        if x == orange_backpack_x and y == orange_backpack_y:
            dora_size -= 1
            orange_backpack_x, orange_backpack_y = generate_orange_backpack()

        # Update Dora's pixels
        pixels.append([x, y])
        if len(pixels) > dora_size:
            del pixels[0]

        # Check collision with herself
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                game_over = True

        # Draw elements on screen
        draw_dora(SQUARE_SIZE, pixels)
        draw_backpack1(SQUARE_SIZE, backpack_x, backpack_y)
        draw_orange_backpack(SQUARE_SIZE, orange_backpack_x, orange_backpack_y)
        draw_score(dora_size)

        pygame.display.update()
        clock.tick(speed)

# Start the game
run_game()

pygame.quit()
