import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_GAP = 100
GRAVITY = 1
BIRD_JUMP = -10
FPS = 30
WHITE = (255, 255, 255)

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PlayBird")

# Menggambar latar belakang
background = pygame.image.load('background.png')

# Menggambar burung
bird = pygame.image.load('bird.png')
bird_rect = bird.get_rect()
bird_x = 50
bird_y = (SCREEN_HEIGHT // 2) - (BIRD_HEIGHT // 2)
bird_speed = 0

# Menggambar pipa
pipe = pygame.image.load('pipe.png')
pipe_x = SCREEN_WIDTH
pipe_height = random.randint(100, 400)

# Menggambar skor
score = 0
font = pygame.font.Font(None, 36)

# Fungsi untuk mengatur permainan
def game_over():
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Loop permainan
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = BIRD_JUMP

    # Menggerakkan burung
    bird_speed += GRAVITY
    bird_y += bird_speed

    # Menggerakkan pipa
    pipe_x -= 5
    if pipe_x < -PIPE_WIDTH:
        pipe_x = SCREEN_WIDTH
        pipe_height = random.randint(100, 400)

    # Memeriksa tabrakan
    if bird_y <= 0 or bird_y >= SCREEN_HEIGHT:
        game_over()

    if bird_x + BIRD_WIDTH >= pipe_x and bird_x <= pipe_x + PIPE_WIDTH:
        if bird_y <= pipe_height or bird_y + BIRD_HEIGHT >= pipe_height + PIPE_GAP:
            game_over()

    # Menggambar latar belakang
    screen.blit(background, (0, 0))

    # Menggambar pipa
    screen.blit(pipe, (pipe_x, 0))
    screen.blit(pipe, (pipe_x, pipe_height + PIPE_GAP))

    # Menggambar burung
    screen.blit(bird, (bird_x, bird_y))

    # Menggambar skor
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2, 50))

    pygame.display.update()

    # Menambah skor
    if pipe_x + PIPE_WIDTH < bird_x and pipe_x + PIPE_WIDTH > bird_x - 5:
        score += 1

    # FPS
    pygame.time.Clock().tick(FPS)
