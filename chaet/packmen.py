import pygame 
import time
import math
import random
from enum import Enum

pygame.init()

weight = 800
height = 600

screen = pygame.display.set_mode((weight,height))
pygame.display.set_caption("стратегия")

GREENSVET = (100, 255, 100)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (0, 120, 255)
DARK_BLUE = (0, 70, 140)
PURPLE = (180, 0, 180)

rec = 0
wave = 1
enemies_in_wave = 2
base_hp = 10000
max_base_hp = 10000
max_allies = 5
base_attack_cooldown = 0  # Кулдаун атаки базы

font = pygame.font.SysFont(None, 76)
font1 = pygame.font.SysFont(None, 36)
font2 = pygame.font.SysFont(None, 28)

class UnitType(Enum):
    WARRIOR = "warrior"
    ENEMY_WARRIOR = "enemy_warrior"

class Unit:
    def __init__(self, x, y, color, unit_type, is_enemy=False):
        self.x = x
        self.y = y
        self.color = color
        self.unit_type = unit_type
        self.is_enemy = is_enemy
        self.vx = 0
        self.vy = 0
        self.target = None
        self.target_is_base = False  # Флаг что цель - база
        self.attack_cooldown = 0
        self.hp = 100
        self.max_hp = 100
        
        # Боевые параметры
        if unit_type == UnitType.WARRIOR:
            self.radius = 15
            self.speed = 2.0
            self.damage = 10
            self.attack_range = 50
            self.mass = 1.0
        elif unit_type == UnitType.ENEMY_WARRIOR:
            self.radius = 15
            self.speed = 1.8
            self.damage = 8
            self.attack_range = 50
            self.mass = 1.0
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Отрисовка обводки
        border_color = (255, 0, 0) if self.is_enemy else (200, 200, 200)
        pygame.draw.circle(screen, border_color, (int(self.x), int(self.y)), self.radius + 1, 2)
        
        # Отрисовка здоровья
        health_width = 30
        health_height = 5
        health_x = self.x - health_width // 2
        health_y = self.y - self.radius - 10
        health_percent = max(0, self.hp / self.max_hp)
        
        # Фон полоски здоровья
        pygame.draw.rect(screen, (100, 100, 100), 
                        (health_x, health_y, health_width, health_height))
        # Само здоровье
        health_color = (255, 0, 0) if self.is_enemy else (0, 255, 0)
        pygame.draw.rect(screen, health_color, 
                        (health_x, health_y, int(health_width * health_percent), health_height))
    
    def update(self, units, dt, base_x, base_y, base_radius):
        # Обновляем кулдаун атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # ИИ для врагов
        if self.is_enemy:
            # Ищем цель: ближайший союзник или база
            if not self.target or (self.target and self.target.hp <= 0):
                self.find_target(units, base_x, base_y)
            
            if self.target_is_base:
                # Цель - база
                # Двигаемся к базе
                dx = base_x - self.x
                dy = base_y - self.y
                distance_to_base = math.sqrt(dx*dx + dy*dy)
                
                if distance_to_base > 0:
                    dx /= distance_to_base
                    dy /= distance_to_base
                
                self.vx = dx * self.speed
                self.vy = dy * self.speed
                
                # Если близко к базе, атакуем
                if distance_to_base <= self.attack_range + base_radius:
                    global base_hp
                    if self.attack_cooldown <= 0:
                        base_hp -= self.damage
                        self.attack_cooldown = 30
            elif self.target and self.target.hp > 0:
                # Цель - союзник
                self.move_towards_target()
                self.attack_target()
        else:
            # ИИ для союзников: ищем врагов
            if not self.target or self.target.hp <= 0:
                self.find_enemy_target(units)
            
            if self.target and self.target.hp > 0:
                self.move_towards_target()
                self.attack_target()
        
        # Применяем скорость
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        
        # Проверяем столкновения с границами
        self.check_boundary_collisions()
        
        # Проверяем столкновения с другими юнитами
        self.check_unit_collisions(units)
        
        # Постепенно замедляем скорость
        self.vx *= 0.95
        self.vy *= 0.95
        
        # Удаляем юнитов с нулевым здоровьем
        return self.hp > 0
    
    def find_target(self, units, base_x, base_y):
        closest_distance = float('inf')
        closest_target = None
        
        # Ищем ближайшего союзника
        for unit in units:
            if not unit.is_enemy and unit.hp > 0:
                dx = unit.x - self.x
                dy = unit.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < closest_distance:
                    closest_distance = distance
                    closest_target = unit
        
        # Если союзник ближе 150 пикселей, атакуем его, иначе базу
        if closest_distance < 150:
            self.target = closest_target
            self.target_is_base = False
        else:
            self.target = None
            self.target_is_base = True  # Специальный флаг для базы
    
    def find_enemy_target(self, units):
        closest_distance = float('inf')
        closest_target = None
        
        for unit in units:
            if unit.is_enemy and unit.hp > 0:
                dx = unit.x - self.x
                dy = unit.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < closest_distance:
                    closest_distance = distance
                    closest_target = unit
        
        self.target = closest_target
        self.target_is_base = False
    
    def move_towards_target(self):
        if not self.target or self.target.hp <= 0:
            return
            
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Если цель в радиусе атаки, не двигаемся
        if distance <= self.attack_range:
            self.vx = 0
            self.vy = 0
            return
        
        # Нормализуем вектор направления
        if distance > 0:
            dx /= distance
            dy /= distance
        
        # Двигаемся к цели
        self.vx = dx * self.speed
        self.vy = dy * self.speed
    
    def attack_target(self):
        if not self.target or self.target.hp <= 0 or self.attack_cooldown > 0:
            return
            
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Если цель в радиусе атаки, атакуем
        if distance <= self.attack_range:
            self.target.hp -= self.damage
            self.attack_cooldown = 30
    
    def check_boundary_collisions(self):
        # Столкновение с левой границей
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx) * 0.8
        
        # Столкновение с правой границей
        if self.x + self.radius > weight:
            self.x = weight - self.radius
            self.vx = -abs(self.vx) * 0.8
        
        # Столкновение с верхней границей
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy) * 0.8
        
        # Столкновение с нижней границей (голубой прямоугольник)
        if self.y + self.radius > rect_area.y:
            self.y = rect_area.y - self.radius
            self.vy = -abs(self.vy) * 0.8
    
    def check_unit_collisions(self, units):
        for other in units:
            if other != self and other.hp > 0:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                min_distance = self.radius + other.radius
                
                if distance < min_distance and distance > 0:
                    overlap = min_distance - distance
                    angle = math.atan2(dy, dx)
                    
                    total_mass = self.mass + other.mass
                    move_self = overlap * (other.mass / total_mass)
                    move_other = overlap * (self.mass / total_mass)
                    
                    self.x -= math.cos(angle) * move_self * 0.5
                    self.y -= math.sin(angle) * move_self * 0.5
                    other.x += math.cos(angle) * move_other * 0.5
                    other.y += math.sin(angle) * move_other * 0.5
                    
                    force = 0.3
                    self.vx -= math.cos(angle) * force * (other.mass / total_mass)
                    self.vy -= math.sin(angle) * force * (other.mass / total_mass)
                    other.vx += math.cos(angle) * force * (self.mass / total_mass)
                    other.vy += math.sin(angle) * force * (self.mass / total_mass)

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
units = []  # Список для хранения всех юнитов

# База - простой круг
base_x = weight // 2
base_y = height // 2
base_radius = 40

text_surface = font.render("Статегия", True, (255, 228, 225))
text_rect = text_surface.get_rect(center=(400, 80))

rec_rect = pygame.Rect(10, 500, 200, 40)

# Голубой прямоугольник (интерфейсная панель)
rect_area = pygame.Rect(0, 450, 800, 200)

Running = True
last_time = time.time()
resource_timer = 0
wave_timer = 0
wave_active = False
enemies_spawned = 0

def base_attack_enemies(units, dt):
    global base_attack_cooldown
    
    if base_attack_cooldown > 0:
        base_attack_cooldown -= dt * 60
    
    # Ищем ближайшего врага в радиусе базы
    closest_enemy = None
    closest_distance = float('inf')
    
    for unit in units:
        if unit.is_enemy and unit.hp > 0:
            dx = unit.x - base_x
            dy = unit.y - base_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Враг считается "в базе" если он очень близко
            if distance <= base_radius + unit.radius + 20:  # +20 для небольшого запаса
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = unit
    
    # Атакуем ближайшего врага в базе раз в 2 секунды (медленно)
    if closest_enemy and base_attack_cooldown <= 0:
        closest_enemy.hp -= 5  # Маленький урон
        base_attack_cooldown = 120  # 2 секунды при 60 FPS
        return closest_enemy
    
    return None

while Running:
    current_time = time.time()
    dt = current_time - last_time
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
                        if rec >= 20:
                            # Проверяем ограничение по количеству союзников
                            current_allies = sum(1 for unit in units if not unit.is_enemy and unit.hp > 0)
                            if current_allies < max_allies:
                                rec -= 20
                                offset_x = random.randint(-100, 100)
                                offset_y = random.randint(-100, 100)
                                new_unit = Unit(weight // 2 + offset_x, height // 2 + offset_y, 
                                              BLUE, UnitType.WARRIOR, False)
                                units.append(new_unit)
                                print(f"Создан союзный воин. Осталось ресурсов: {rec}")
                            else:
                                print(f"Достигнут лимит союзников: {max_allies}")

    if game_started:
        # Проверка поражения
        if base_hp <= 0:
            game_started = False
            units = []
            rec = 0
            wave = 1
            enemies_in_wave = 2
            max_allies = 5
            base_hp = max_base_hp
            print("База уничтожена! Игра окончена.")
        
        # Автоматическое накопление ресурсов каждую секунду
        resource_timer += dt
        if resource_timer >= 1.0:
            rec += 10
            resource_timer = 0
        
        # Логика волн - каждые 10 секунд
        if not wave_active:
            wave_timer += dt
            if wave_timer >= 10.0:  # Волна каждые 10 секунд
                wave_active = True
                enemies_spawned = 0
                wave_timer = 0
                print(f"Начинается волна {wave}! Врагов: {enemies_in_wave}")
        else:
            # Спавн ВСЕХ врагов сразу при начале волны
            if enemies_spawned == 0:
                # Создаем всех врагов сразу с разных сторон
                for i in range(enemies_in_wave):
                    # Распределяем врагов по разным сторонам
                    side = i % 4  # 0-верх, 1-право, 2-низ, 3-лево
                    
                    if side == 0:  # Сверху
                        enemy_x = random.randint(50, weight - 50)
                        enemy_y = random.randint(30, 80)
                    elif side == 1:  # Справа
                        enemy_x = random.randint(weight - 100, weight - 50)
                        enemy_y = random.randint(50, rect_area.y - 50)
                    elif side == 2:  # Снизу
                        enemy_x = random.randint(50, weight - 50)
                        enemy_y = random.randint(rect_area.y - 100, rect_area.y - 50)
                    else:  # Слева
                        enemy_x = random.randint(30, 80)
                        enemy_y = random.randint(50, rect_area.y - 50)
                    
                    enemy = Unit(enemy_x, enemy_y, RED, UnitType.ENEMY_WARRIOR, True)
                    units.append(enemy)
                
                enemies_spawned = enemies_in_wave
                print(f"Создано {enemies_in_wave} врагов со всех сторон!")
            
            # Проверяем, все ли враги убиты
            enemy_count = sum(1 for unit in units if unit.is_enemy and unit.hp > 0)
            if enemy_count == 0:
                wave_active = False
                wave_timer = 0
                # Увеличиваем количество врагов для следующей волны
                wave += 1
                enemies_in_wave = 2 ** wave  # 2, 4, 8, 16...
                
                # Увеличиваем лимит союзников на 1 за каждую волну
                max_allies += 1
                
                # Награда за волну
                rec += 50 * wave
                print(f"Волна {wave-1} завершена! Начинается волна {wave}. Врагов: {enemies_in_wave}")
                print(f"Лимит союзников увеличен до: {max_allies}")
        
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (8, 255, 197), rect_area)
        
        # База атакует врагов
        attacked_enemy = base_attack_enemies(units, dt)
        
        # Рисуем базу - простой круг
        base_color = DARK_BLUE
        if base_hp < max_base_hp * 0.3:
            base_color = (200, 50, 50)  # Красный при низком HP
        elif base_hp < max_base_hp * 0.6:
            base_color = (200, 150, 50)  # Оранжевый при среднем HP
        
        pygame.draw.circle(screen, base_color, (base_x, base_y), base_radius)
        pygame.draw.circle(screen, (100, 150, 255), (base_x, base_y), base_radius, 3)
        
        # Внутренний круг базы
        pygame.draw.circle(screen, (150, 200, 255), (base_x, base_y), base_radius - 10)
        
        # Если база атакует, рисуем эффект атаки
        if attacked_enemy:
            # Линия от базы к врагу
            pygame.draw.line(screen, PURPLE, (base_x, base_y), 
                           (attacked_enemy.x, attacked_enemy.y), 3)
            # Эффект вокруг базы
            pygame.draw.circle(screen, (255, 100, 255, 128), 
                             (base_x, base_y), base_radius + 10, 2)
        
        # Полоска здоровья базы
        base_health_width = 100
        base_health_height = 10
        base_health_x = base_x - base_health_width // 2
        base_health_y = base_y - base_radius - 20
        base_health_percent = max(0, base_hp / max_base_hp)
        
        pygame.draw.rect(screen, (50, 50, 50), 
                        (base_health_x, base_health_y, base_health_width, base_health_height))
        pygame.draw.rect(screen, (0, 255, 0) if base_health_percent > 0.5 else 
                        (255, 255, 0) if base_health_percent > 0.2 else (255, 0, 0), 
                        (base_health_x, base_health_y, int(base_health_width * base_health_percent), base_health_height))
        
        # Текст HP базы
        base_hp_text = font2.render(f"{int(base_hp)}/{max_base_hp}", True, WHITE)
        screen.blit(base_hp_text, (base_x - base_hp_text.get_width()//2, base_y - base_radius - 35))
        
        # Отрисовка кнопки создания юнита
        current_allies = sum(1 for unit in units if not unit.is_enemy and unit.hp > 0)
        if current_allies >= max_allies:
            create_unit_color = (100, 100, 100)  # Серый при достижении лимита
            create_unit_text = font1.render(f"Лимит: {max_allies}", True, (200, 200, 200))
        else:
            create_unit_color = (100, 100, 255)
            create_unit_text = font1.render("Создать юнита (-20)", True, WHITE)
        
        pygame.draw.rect(screen, create_unit_color, create_unit_button)
        screen.blit(create_unit_text, create_unit_textren)
        
        # Отображение ресурсов
        rec_surface = font1.render(f"Ресурсы: {rec}", True, (57, 8, 255))
        screen.blit(rec_surface, (rec_rect.x, rec_rect.y))
        
        # Отображение таймера и волны
        if wave_active:
            wave_text = font1.render(f"Волна {wave} идет!", True, RED)
        else:
            time_left = max(0, 10 - wave_timer)
            wave_text = font1.render(f"Волна {wave} через: {time_left:.1f}с", True, GREEN)
        screen.blit(wave_text, (weight - 250, 50))
        
        # Обновление и отрисовка всех юнитов
        units_to_remove = []
        for i, unit in enumerate(units):
            if not unit.update(units, dt, base_x, base_y, base_radius):
                units_to_remove.append(i)
            else:
                unit.draw(screen)
        
        # Удаление мертвых юнитов
        for index in sorted(units_to_remove, reverse=True):
            units.pop(index)
        
        # Отображение статистики
        ally_count = sum(1 for unit in units if not unit.is_enemy and unit.hp > 0)
        enemy_count = sum(1 for unit in units if unit.is_enemy and unit.hp > 0)
        
        stats_text = font1.render(f"Наших: {ally_count}/{max_allies}  Врагов: {enemy_count}", True, WHITE)
        screen.blit(stats_text, (weight - 300, 10))
        
        # Отображение волны
        wave_info = font1.render(f"Волна: {wave}", True, (255, 255, 100))
        screen.blit(wave_info, (10, 10))
                
    else: 
        screen.fill((40, 40, 41))
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, start_color, start_buton)
        screen.blit(start_text, start_textren)
        pygame.draw.rect(screen, exit_color, exit_buton)
        screen.blit(exit_text, exit_textren)
    
    pygame.display.flip()

pygame.quit()