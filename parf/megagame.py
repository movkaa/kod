import pygame
import random
import math

pygame.init()
widght=800
height=600

scree = pygame.display.set_mode((widght,height))
pygame.display.set_caption("Космческий защитник")
player=(0,255,0)
vrag=(255,0,0)
fon=(0,0,0)
healt_pack_color=(235,255,0)
bulletcol=(255, 255, 0)
textcol = (255,0,100)

#игрок
class Player:
    def __init__(self):
        self.size = 40
        self.x = widght//2
        self.y = height - 100
        self.speed = 8
        self.healt = 3
        self.max_healt = 5

        self.surface = pygame.Surface((self.size,self.size), pygame.SRCALPHA)

        self.points = [
            (self.size//2,0),
            (0,self.size),
            (self.size,self.size)
        ]

        pygame.draw.polygon(self.surface,player,self.points)

        self.mask = pygame.mask.from_surface(self.surface)

        self.rect = pygame.Rect(self.x,self.y,self.size,self.size)

    def draw(self, scree):
        scree.blit(self.surface,(self.x,self.y))
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -=self.speed

        if keys[pygame.K_RIGHT] and self.x < widght - self.size:
            self.x +=self.speed

        if keys[pygame.K_UP] and self.y > 0:
            self.y -=self.speed

        if keys[pygame.K_DOWN] and self.y < height - self.size:
            self.y +=self.speed


class Enemy:
    def __init__(self, x, y):
        self.size = 10
        self.x = x
        self.y = y
        self.speed = 10

        self.surface = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        pygame.draw.rect(self.surface,vrag,(0,0, self.size, self.size))
        self.mask = pygame.mask.from_surface(self.surface)
        self.rect = pygame.Rect(self.x,self.y,self.size, self.size)

    def update(self):
            self.y += self.speed
            self.rect.y = self.y

    def draw(self, scree):
            scree.blit(self.surface, (self.x, self.y))

    def is_off_screen(self):
            return self.y > height

class Bullet:
    def __init__(self,x,y):
        self.size = 10
        self.x = x
        self.y = y
        self.speed = 100

        self.surface = pygame.Surface((self.size, self.size),pygame.SRCALPHA)
        pygame.draw.rect(self.surface,bulletcol,(0,0, self.size, self.size))
        self.mask = pygame.mask.from_surface(self.surface)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.y -=self.speed
        self.rect.y = self.y

    def draw(self, scree):
        scree.blit(self.surface,(self.x, self.y))
    def is_off_screen(self):
        return self.y < -self.size

class Healt_pack:
    def __init__(self, x,y):
        self.size = 25 
        self.x = x
        self.y = y
        self.speed = 10

        self.surface = pygame.Surface((self.size, self.size),pygame.SRCALPHA)

        pygame.draw.rect(self.surface, healt_pack_color,(self.size//4, 0, self.size//2, self.size))
        pygame.draw.rect(self.surface, healt_pack_color,(0, self.size//4, self.size, self.size//2))   
        self.mask = pygame.mask.from_surface(self.surface)
        self.rect = pygame.Rect(self.x,self.y,self.size,self.size)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y
    
    def draw(self, scree):    
        scree.blit(self.surface,(self.x, self.y))

    def is_off_screen(self):
        return self.y > height


player = Player()
enemies = []
bullets = []
healt_packs = []

enemy_spawn_rate = 3
healt_spawn_rate = 200
bullets_cooldown = 0  
bullets_cooldown_max = 1

clock = pygame.time.Clock()
score = 0
Running = True
game_over = False

font = pygame.font.SysFont(None,36)

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE and bullets_cooldown == 0:
                bullet_x = player.x + player.size // 2 - 4
                bullet_y = player.y
                bullets.append(Bullet(bullet_x,bullet_y))
                bullets_cooldown = bullets_cooldown_max
    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)

        if bullets_cooldown > 0:
            bullets_cooldown -= 1
        if random.randint(1, enemy_spawn_rate) == 1:
            enemy_x = random.randint(0, widght -30)
            enemies.append(Enemy(enemy_x, -30))
        if random.randint(1, healt_spawn_rate) == 1:
            healt_x = random.randint(0, widght - 25)
            healt_packs.append(Healt_pack(healt_x, -25))

        for enemy in enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                enemies.remove(enemy) 

        for bullet in bullets[:]:
            bullet.update()

        for healt_pack in healt_packs[:]:
            healt_pack.update()
            if healt_pack.is_off_screen():
                healt_packs.remove(healt_pack)

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    offset_x = enemy.x - bullet.x
                    offset_y = enemy.y - bullet.y
                    if bullet.mask.overlap(enemy.mask,(offset_x, offset_y)):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 10
                        break

        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                offset_x = enemy.x - player.x
                offset_y = enemy.y - player.y

                if player.mask.overlap(enemy.mask,(offset_x, offset_y)):
                    enemies.remove(enemy)
                    player.healt -=1

                    

                    if player.healt<= 0:
                        game_over = True

        for healt_pack in healt_packs[:]:
            if player.rect.colliderect(healt_pack.rect):
                offset_x = healt_pack.x - player.x
                offset_y = healt_pack.y - player.y

                if player.mask.overlap(healt_pack.mask,(offset_x,offset_y)):
                    healt_packs.remove(healt_pack)
                    if player.healt < player.max_healt:
                        player.healt +=1
            
        scree.fill(fon)

        for enemy in enemies:
            enemy.draw(scree)
        
        for bullet in bullets:
            bullet.draw(scree)

        for healt_pack in healt_packs:
            healt_pack.draw(scree)

        player.draw(scree)

        heatlh_text = font.render(f'Жизни:{player.healt}',True,textcol)
        scree.blit(heatlh_text,(10,50))

        score_text = font.render(f'Счет:{score}',True,textcol)
        scree.blit(score_text,(10,10))

        if game_over:
            game_over_text = font.render("игра окончена! R для перезапуска",True,textcol)
            scree.blit(game_over_text,(widght // 2-200,height // 2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                
                player = Player()
                enemies.clear()
                bullets.clear()
                health_packs.clear()
                score = 0
                game_over = False
            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
                
