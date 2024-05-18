import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
import os


pygame.init()

HEIGTH = 700
WIDTH = 1200

background = pygame.transform.scale(pygame.image.load('../images/background.png'), (WIDTH, HEIGTH))
bg_X1 = 0
bg_X2 = background.get_width()
bg_move = 3

FONT = pygame.font.SysFont('Arial', 20, 600)

FPS = pygame.time.Clock()
main_display = pygame.display.set_mode((WIDTH, HEIGTH))
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_blue = (0, 0, 255)
color_green = (0, 255, 0)

IMAGE_PATH = '../images/goose_animation'
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (30, 30)
player = pygame.image.load('../images/player.png')
player_rect = player.get_rect()
player_rect.centery = HEIGTH // 2
player_rect.centerx = WIDTH - 1000
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

def create_bonus():
    bonus_size = (60, 60)
    bonus = pygame.image.load('../images/bonus.png')
    bonus_rect = pygame.Rect(random.randint(50, WIDTH-50), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load('../images/enemy.png')
    enemy_rect = pygame.Rect(WIDTH, random.randint(50, HEIGTH-50), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_BONUS = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_BONUS, 3000)

CREATE_ENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_PLAYER = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_PLAYER, 200)

bonuses = []
enemies = []
playing = True
score = 0
image_index = 0

while playing:
    FPS.tick(200)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_PLAYER:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -background.get_width():
        bg_X1 = background.get_width()

    if bg_X2 < -background.get_width():
        bg_X2 = background.get_width()

    main_display.blit(background, (bg_X1, 0))
    main_display.blit(background, (bg_X2, 0))
    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGTH:
        player_rect = player_rect.move(player_move_down)
    
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    main_display.blit(FONT.render(str(score), True, color_black), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGTH:
            bonuses.pop(bonuses.index(bonus))