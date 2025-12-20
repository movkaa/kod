import pygame
import random

pygame.init()
scree = pygame.display.set_mode((800,600))
pygame.display.set_caption("игры")
player=(0,255,0)
vrag=(255,0,0)
fon=(0,0,0)
healt_pack_color=(255,255,255)
#игрок
player_size = 40
player_x = 800//2 - player_size//2
player_y = 500
player_speed = 12
healt = 3

enem = []
enem_size = 20
enem_speed = 5
spawn_rate =10

heat= []
healt_pack_size = 20
healt_pack_speed = 10
healt_pack_spawn = 10

clock = pygame.time.Clock()
score = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys [pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x +=player_speed

    if random.randint(1, spawn_rate) == 1:
        enem_x = random.randint(0, 800 - enem_size)
        enem.append([enem_x, - enem_size])

    if random.randint(1, healt_pack_spawn) == 1:
        heat_x = random.randint(0, 800 - healt_pack_size)
        heat.append([heat_x, - healt_pack_size])

    for enemy in enem[:]:
        enemy[1] += enem_speed
        if(player_x < enemy[0] + enem_size and
        player_x + player_size >  enemy[0] and
        player_y < enemy[1] + enem_size and
        player_y + player_size > enemy[1]):
            score+=1
            enem.remove(enemy)
        

        if enemy[1] > 800:
            enem.remove(enemy)
            score-=1
            if score == 0:
             running = False

    scree.fill(fon)

    pygame.draw.rect(scree,  player, (player_x, player_y, player_size, player_size))
    for healt_pack in heat:
        pygame.draw.rect(scree,  healt_pack_color, (healt_pack[0], healt_pack[1], healt_pack_size, healt_pack_size))
    for enemy in enem:
        pygame.draw.rect(scree, vrag, (enemy[0],  enemy[1], enem_size, enem_size))


    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Счёт:{score}",True, (255,255,255))
    scree.blit(score_text, (10,10))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()