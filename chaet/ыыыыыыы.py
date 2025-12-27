import pygame 
import time
from enum import Enum

pygame.init()

weight = 800
height = 600

screen = pygame.display.set_mode((weight,height))
pygame.display.set_caption("стратегия")

GREENSVET = (100, 255, 100)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

rec = 0
font = pygame.font.SysFont(None, 76)
font1 = pygame.font.SysFont(None, 36)

class UnitType(Enum):
    WARRIOR = "warrior"
    ARCHER = "archer"
    TANK = "tank"

class Unit:
    def __init__(self, x, y, color, unit_type):
        self.x = x
        self.y = y
        self.color = color
        self.unit_type = unit_type
        
        # Боевые параметры
        if unit_type == UnitType.WARRIOR:
            self.radius = 10
            self.speed = 200
            self.max_hp = 1200
            self.hp = self.max_hp
            self.damage = 150
            self.attack_range = 350
            self.attack_cooldown = 0
        elif unit_type == UnitType.ARCHER:
            self.radius = 12
            self.speed = 2.5
            self.max_hp = 80
            self.hp = self.max_hp
            self.damage = 8
            self.attack_range = 120
            self.attack_cooldown = 40
        elif unit_type == UnitType.TANK:
            self.radius = 20
            self.speed = 1.5
            self.max_hp = 200
            self.hp = self.max_hp
            self.damage = 20
            self.attack_range = 25
            self.attack_cooldown = 90
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Отрисовка здоровья
        pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), self.radius + 1, 2)

# Кнопка "Начать"
start_buton = pygame.Rect(300, 250, 200, 50)
start_color = GREEN
start_text = font1.render("Начать", True, WHITE)
start_textren = start_text.get_rect(center=start_buton.center)

exit_buton = pygame.Rect(300, 350, 200, 50)
exit_color = ((178, 34, 34))
exit_text = font1.render("Выход", True, (255, 228, 225))
exit_textren = exit_text.get_rect(center=exit_buton.center)

# Кнопка "Создать юнита"
create_unit_button = pygame.Rect(220, 510, 300, 50)
create_unit_color = (100, 100, 255)
create_unit_text = font1.render("Создать юнита (-20)", True, WHITE)
create_unit_textren = create_unit_text.get_rect(center=create_unit_button.center)

game_started = False
units = []  # Список для хранения созданных юнитов

text_surface = font.render("Статегия", True, (255, 228, 225))
text_rect = text_surface.get_rect(center=(400, 80))

rec_rect = pygame.Rect(10, 500, 200, 40)  # Область для отображения ресурсов

rect_area = pygame.Rect(0, 450, 800, 200)

Running = True
last_time = time.time()

while Running:
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        if event.type == pygame.MOUSEMOTION:
            if not game_started:
                if start_buton.collidepoint(event.pos):
                    start_color = ((0, 250, 154))
                else:
                    start_color = GREEN
                if exit_buton.collidepoint(event.pos):
                    exit_color = ((139, 0, 0))
                else:
                    exit_color = ((178, 34, 34))
            else:
                if create_unit_button.collidepoint(event.pos):
                    create_unit_color = (150, 150, 255)
                else:
                    create_unit_color = (100, 100, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not game_started:
                    if start_buton.collidepoint(event.pos):
                        game_started = True
                        print("старт")
                    if exit_buton.collidepoint(event.pos):
                        Running = False
                else:
                    if create_unit_button.collidepoint(event.pos):
                        if rec >= 20:  # Проверяем, достаточно ли ресурсов
                            rec -= 20  # Вычитаем 20 ресурсов
                            # Создаем юнит WARRIOR в середине экрана
                            new_unit = Unit(weight // 2, height // 2, (0, 0, 255), UnitType.WARRIOR)
                            units.append(new_unit)
                            print(f"Создан юнит WARRIOR. Осталось ресурсов: {rec}")

    if game_started:
        # Автоматическое накопление ресурсов каждую секунду
        time.sleep(1)
        rec += 1
        
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (8, 255, 197), rect_area)
        
        # Отрисовка кнопки создания юнита
        pygame.draw.rect(screen, create_unit_color, create_unit_button)
        screen.blit(create_unit_text, create_unit_textren)
        
        # Отображение ресурсов рядом с кнопкой
        rec_surface = font1.render(f"Ресурсы: {rec}", True, (57, 8, 255))
        screen.blit(rec_surface, (rec_rect.x, rec_rect.y))
        
        # Отрисовка всех юнитов
        for unit in units:
            unit.draw(screen)
                
    else: 
        screen.fill((40, 40, 41))
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, start_color, start_buton)
        screen.blit(start_text, start_textren)
        pygame.draw.rect(screen, exit_color, exit_buton)
        screen.blit(exit_text, exit_textren)
    
    pygame.display.flip()

pygame.quit()