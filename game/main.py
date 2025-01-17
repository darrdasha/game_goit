import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()

FPS = pygame.time.Clock()


HEIGHT = 600
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WIGHT = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (225, 0, 0)
COLOR_GREEN = (0, 255, 0)

main_disolay = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bgX1 = 0
bgX2 = bg.get_width()
bg_move = 3



player_size  = (70, 50)
player = pygame.transform.scale(pygame.image.load('player.png').convert_alpha(), player_size)
player_rect = pygame.Rect(0, 300, *player_size)

player_move_down = [0, 5]
player_move_top = [0, -5]
player_move_right = [4, 0]
player_move_left = [-4, 0]

def create_enemy():
    enemy_size = (80, 40)
    enemy = pygame.Surface(enemy_size)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), enemy_size)
    enemy_rect = pygame.Rect(WIDTH, random.randint(45, HEIGHT -55),*enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (90, 120)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), bonus_size)
    bonus_rect = pygame.Rect(random.randint(350, WIDTH -420), 0, *bonus_size)
    bonus_move = [0, random.randint(2, 3)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

enemies = []
bonuses = []

score = 0

playing = True

while playing:
    FPS.tick(220)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    bgX1 -= bg_move
    bgX2 -= bg_move

    if bgX1 < -bg.get_width():
        bgX1 = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_disolay.blit(bg, (bgX1, 0))
    main_disolay.blit(bg, (bgX2, 0))

    

    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_top)
    
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_disolay.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_disolay.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
            

    main_disolay.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))

    main_disolay.blit(player, player_rect)
   
    
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0 :
            enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT :
            bonuses.pop(bonuses.index(bonus))