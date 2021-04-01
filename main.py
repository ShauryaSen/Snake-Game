import pygame
import random

pygame.font.init()
pygame.mixer.init()
# **CONSTANTS**
FPS = 10
TOP_PADDING = 70

# COLORS
LIGHT_CHECKER = (170, 215, 81)
DARK_CHECKER = (162,209,73)
TOP_BAR_COLOR = (87, 138, 52)
WHITE = (255, 255, 255)
BLUE = (84, 132, 241)
RED = (255, 0, 0)

# Fonts
GAMEOVER_FONT = pygame.font.SysFont("comicsans", 100)
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

# Homemade game events
GAMEOVER = pygame.USEREVENT + 1
APPLE_EATEN = pygame.USEREVENT + 2

# Window stuff
WIN_WIDTH, WIN_HEIGHT = 595, 525 + TOP_PADDING
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Snake Game")


def draw_game(snake, apple, score):

    alternate = False
    # Draw the checkered board
    for x in range(17):
        for y in range(15):         
            if alternate:
                pygame.draw.rect(WIN, DARK_CHECKER, pygame.Rect(0 + (35 * x), TOP_PADDING + (35 * y), 35, 35))
                alternate = False
            else:
                pygame.draw.rect(WIN, LIGHT_CHECKER, pygame.Rect(0 + (35 * x), TOP_PADDING + (35 * y), 35, 35))
                alternate = True

    # Draw the top bar
    pygame.draw.rect(WIN, TOP_BAR_COLOR, pygame.Rect(0, 0, 595, TOP_PADDING))

    # Score
    score_text = SCORE_FONT.render(f"Score: {str(score)}", 1, WHITE)
    WIN.blit(score_text, (WIN_WIDTH/2 - score_text.get_width()/2, TOP_PADDING/2 - score_text.get_height()/2))

    # Draw an Apple
    pygame.draw.rect(WIN, RED, apple)

    # Draw the Snake
    for cube in snake:
        pygame.draw.rect(WIN, BLUE, cube)

    pygame.display.update()


def snake_move(direction, snake):
    for index in range(len(snake)):
        # if this is the head of the snake, move forward, otherwise follow the rest of the body
        if (index == len(snake) - 1):
            if direction == "up":
                snake[index].y -= 35

            elif direction == "right":
                snake[index].x += 35

            elif direction == "down":
                snake[index].y += 35
            
            elif direction == "left":
                snake[index].x -= 35
        else:
            snake[index].x = snake[index + 1].x
            snake[index].y = snake[index + 1].y


def is_gameover(snake):
    coords = []
    for body in snake:
        if (body.x < 0 or body.x > WIN_WIDTH) or (body.y < TOP_PADDING or body.y > WIN_HEIGHT):
            pygame.event.post(pygame.event.Event(GAMEOVER))
        coords.append((body.x, body.y))
    
    coords_set = set(coords)

    if len(coords_set) != len(coords):
        pygame.event.post(pygame.event.Event(GAMEOVER))

    
def gameover():
    gameover_text = GAMEOVER_FONT.render("GAMEOVER", 1, WHITE)
    WIN.blit(gameover_text, (WIN_WIDTH/2 - gameover_text.get_width()/2, WIN_HEIGHT/2 - gameover_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


def is_apple_eaten(snake, apple):
    snake_head = snake[len(snake) - 1]

    if snake_head.x == apple.x and snake_head.y == apple.y:
        pygame.event.post(pygame.event.Event(APPLE_EATEN))


def main():
    score = 0
    clock = pygame.time.Clock()
    direction = "up"

    # Array of snake body parts (start them off with three)
    snake = [pygame.Rect(280, 490, 35, 35), pygame.Rect(280, 455, 35, 35), pygame.Rect(280, 420, 35, 35)]
    
    # draw the first apple
    random_x = random.randint(0,16) + 1
    random_y = random.randint(0,14) + 1
    apple = pygame.Rect(random_x * 35, random_y * 35 + TOP_PADDING, 35, 35)
    

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    
            #checks if a key just got pressed
            if event.type == pygame.KEYDOWN:
                # which key was it?
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction = "up"
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction = "right"
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction = "down"
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction = "left"
            
            if event.type == APPLE_EATEN:
                random_x = random.randint(0,16) + 1
                random_y = random.randint(0,14) + 1
                apple = pygame.Rect(random_x * 35, random_y * 35 + TOP_PADDING, 35, 35)

                score += 1
                print(score)

                # Make the snake longer
                snake.insert(0, pygame.Rect(-35, -35, 35, 35))

            if event.type == GAMEOVER:
                gameover()
                main()

        is_apple_eaten(snake, apple)
        snake_move(direction, snake) 
        draw_game(snake, apple, score)
        is_gameover(snake)
        
    main()
        
                

if __name__ == "__main__":
    main()