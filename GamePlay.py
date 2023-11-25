from tkinter import *
from tkinter.ttk import *

from typing import Any
import pygame
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
fps = 60

lebar_layar = 450
tinggi_layar = 680

screen = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption('QuantumQuill Technology')

font = pygame.font.SysFont('PressStart2P-Regular', 45)

white = (255, 255, 255)

ground_scroll = 0
scroll_speed = 5
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1000
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

bg = pygame.image.load('assets/img/flappy-bg.png')
ground_img = pygame.image.load('assets/img/floor-sprite.png')
button_img = pygame.image.load('assets/img/restart.png')
lobby_sound = pygame.mixer.Sound('assets/musik/Loby.wav')
lobby_sound.play(-1) 
score_sound = pygame.mixer.Sound('assets/musik/score.wav')
pass_pipe_sound = pygame.mixer.Sound('assets/musik/sound.wav')
game_over_sound = pygame.mixer.Sound('assets/musik/over.wav')
restart_sound = pygame.mixer.Sound('assets/musik/start.wav')
loading_screen = pygame.image.load('assets/img/loading.jpeg')
is_loading = True
loading_done = False
loading_start_time = pygame.time.get_ticks()  
loading_font = pygame.font.SysFont('PressStart2P-Regular', 25)  # Font untuk tulisan di layar loading

channel_lobby = pygame.mixer.Channel(0)  # Channel untuk suara latar belakang
channel_game_over = pygame.mixer.Channel(1)  # Channel untuk suara game over
channel_score = pygame.mixer.Channel(2)  # Channel untuk suara penambahan skor

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(tinggi_layar / 2)
    flappy.vel = 0  # Reset bird's velocity
    flappy.index = 1  # Reset bird's animation index
    flappy.image = flappy.images[flappy.index]  # Reset bird's image to the first frame
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range (1, 4):
            img = pygame.image.load(f'assets/img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0

    def update(self):
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 550:
                self.rect.y += int(self.vel)

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
            self.counter += 1
            flap_cooldown = 3
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(tinggi_layar / 2))

bird_group.add(flappy)

button = Button(lebar_layar // 2 - 50, tinggi_layar // 2 - 25, button_img)


while is_loading:
    current_time = pygame.time.get_ticks()
    screen.blit(loading_screen, (0, 0))

    # Menampilkan tulisan di tengah layar
    if not loading_done:
        loading_text = "Welcome, Sedang mempersiapkan game! Loading..."
        text_width, text_height = loading_font.size(loading_text)
        text_x = (lebar_layar - text_width) // 2
        text_y = (tinggi_layar - text_height) // 2
        draw_text(loading_text, loading_font, white, text_x, text_y)

    pygame.display.update()

    # Menghitung waktu tampilan loading screen selama 5 detik
    if current_time - loading_start_time >= 5000:
        loading_done = True

    if loading_done:
        is_loading = False  # Keluar dari loop loading setelah 5 detik

run = True
while run:

    clock.tick(fps)

    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, 550))
    
    if not channel_lobby.get_busy():  # Memeriksa apakah channel latar belakang sedang digunakan
        channel_lobby.play(lobby_sound, loops=-1)  # Memainkan suara latar belakang


    # Pemutaran musik latar belakang hanya sebelum permainan dimulai
    if not flying and not game_over:
        if pygame.mixer.get_busy():  # Memeriksa apakah musik sudah berhenti
            lobby_sound.play(-1)  # Melanjutkan pemutaran musik jika sudah berhenti
        else:
            lobby_sound.play(-1)  # Memainkan musik jika belum dimulai
            
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                score_sound.play()  # Memainkan suara khusus untuk penambahan skor
                pass_pipe_sound.play()
            if not channel_score.get_busy():  # Memeriksa apakah channel skor sedang digunakan
                channel_score.play(score_sound)  # Memainkan suara penambahan skor
                
    draw_text(str(score), font, white, int(lebar_layar / 2) , 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        pass_pipe_sound.stop()

    if flappy.rect.bottom >= 550:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        lobby_sound.stop()
        if time_now - last_pipe > pipe_frequency:
            tinggi_pipa = random.randint(-100, 100)
            pipa_bawah = Pipe(lebar_layar, int(tinggi_layar / 2) + tinggi_pipa,-1)
            pipa_atas = Pipe(lebar_layar, int(tinggi_layar / 2) + tinggi_pipa, 1)
            pipe_group.add(pipa_bawah)
            pipe_group.add(pipa_atas)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    if game_over == True:
        channel_lobby.stop()  # Menghentikan suara latar belakang
        channel_game_over.play(game_over_sound)  # Memainkan suara game over
        if button.draw() == True:
            game_over = False
            score = reset_game()
            restart_sound.play()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()
    
pygame.quit()
