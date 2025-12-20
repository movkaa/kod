import pygame
import sys
import math
import random
from enum import Enum

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
WAVE_INTERVAL = 30  # секунд между волнами

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
GRAY = (100, 100, 100)
LIGHT_BLUE = (100, 150, 255)
DARK_GREEN = (30, 60, 30)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)
YELLOW = (255, 255, 50)
ORANGE = (255, 150, 50)
PURPLE = (180, 70, 220)
DARK_RED = (150, 0, 0)
BROWN = (139, 69, 19)

class UnitType(Enum):
    WARRIOR = "warrior"
    ARCHER = "archer"
    TANK = "tank"

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.color = BUTTON_HOVER
            return True
        self.color = BUTTON_COLOR
        return False
        
    def is_clicked(self, pos, event):
        return self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN

class HealthBar:
    def __init__(self, unit):
        self.unit = unit
        self.width = unit.radius * 2
        self.height = 5
        
    def draw(self, screen):
        # Фон полоски здоровья
        x = self.unit.x - self.width // 2
        y = self.unit.y - self.unit.radius - 10
        pygame.draw.rect(screen, (100, 0, 0), (x, y, self.width, self.height))
        
        # Текущее здоровье
        health_width = int((self.unit.hp / self.unit.max_hp) * self.width)
        health_color = GREEN if self.unit.hp > self.unit.max_hp * 0.5 else ORANGE if self.unit.hp > self.unit.max_hp * 0.25 else RED
        pygame.draw.rect(screen, health_color, (x, y, health_width, self.height))

class Unit:
    def __init__(self, x, y, color, team, unit_type):
        self.x = x
        self.y = y
        self.team = team
        self.color = color
        self.selected = False
        self.unit_type = unit_type
        
        # Боевые параметры
        if unit_type == UnitType.WARRIOR:
            self.radius = 15
            self.speed = 2.0
            self.max_hp = 120
            self.hp = self.max_hp
            self.damage = 15
            self.attack_range = 35
            self.attack_cooldown = 60
            self.color = BLUE if team == 1 else RED
        elif unit_type == UnitType.ARCHER:
            self.radius = 12
            self.speed = 2.5
            self.max_hp = 80
            self.hp = self.max_hp
            self.damage = 8
            self.attack_range = 120
            self.attack_cooldown = 40
            self.color = GREEN if team == 1 else ORANGE
        elif unit_type == UnitType.TANK:
            self.radius = 20
            self.speed = 1.5
            self.max_hp = 200
            self.hp = self.max_hp
            self.damage = 20
            self.attack_range = 25
            self.attack_cooldown = 90
            self.color = PURPLE if team == 1 else BROWN
        
        self.target_x = x
        self.target_y = y
        self.target_enemy = None
        self.health_bar = HealthBar(self)
        self.attack_timer = 0
        self.idle_time = 0
        
    def draw(self, screen):
        # Тело юнита
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Дополнительные детали для разных типов
        if self.unit_type == UnitType.ARCHER:
            # Лук у лучников
            pygame.draw.rect(screen, BROWN, (int(self.x)-8, int(self.y)-2, 16, 4))
        elif self.unit_type == UnitType.TANK:
            # Броня у танков
            pygame.draw.circle(screen, (50, 50, 50), (int(self.x), int(self.y)), self.radius, 3)
        
        # Контур если выбран
        if self.selected:
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius + 2, 2)
            # Радиус атаки (только для выбранных)
            pygame.draw.circle(screen, (255, 0, 0, 100), (int(self.x), int(self.y)), self.attack_range, 1)
            
        # Полоска здоровья
        if self.hp < self.max_hp:  # Показываем только если ранены
            self.health_bar.draw(screen)
            
    def update(self, units):
        # Обновляем таймер атаки
        if self.attack_timer > 0:
            self.attack_timer -= 1
            
        # Если враг и есть цель, проверяем что цель жива
        if self.team == 2:  # Враги
            if self.target_enemy and self.target_enemy.hp <= 0:
                self.target_enemy = None
                self.idle_time = 0
            
        # Поиск цели если нет текущей цели или цель мертва
        if not self.target_enemy or (self.target_enemy.hp <= 0 and self.team == 1):
            self.find_target(units)
            
        # Если есть цель, пытаемся атаковать
        if self.target_enemy and self.target_enemy.hp > 0:
            distance = self.distance_to(self.target_enemy)
            
            if distance <= self.attack_range:
                # Атакуем если можем
                self.attack(self.target_enemy)
                self.idle_time = 0
            else:
                # Двигаемся к цели
                self.move_towards(self.target_enemy.x, self.target_enemy.y)
                self.idle_time = 0
        else:
            # Если нет цели, двигаемся к заданной точке или патрулируем
            if self.team == 1:  # Игрок
                self.move_to_target()
            else:  # Враг
                # Враги патрулируют или двигаются к базе игрока
                self.idle_time += 1
                if self.idle_time > 60:  # 1 секунда без цели
                    self.patrol()
                    
        # Применяем физику столкновений
        self.resolve_collisions(units)
        
    def move_to_target(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > self.speed:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed
            
    def move_towards(self, tx, ty):
        dx = tx - self.x
        dy = ty - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > self.speed:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed
            
    def patrol(self):
        # Случайное движение для врагов
        if random.random() < 0.02:  # 2% шанс сменить направление
            self.target_x = self.x + random.randint(-100, 100)
            self.target_y = self.y + random.randint(-100, 100)
            
        # Ограничиваем в пределах игровой зоны
        self.target_x = max(50, min(SCREEN_WIDTH - 50, self.target_x))
        self.target_y = max(50, min(SCREEN_HEIGHT - 150, self.target_y))
        
        self.move_to_target()
            
    def find_target(self, units):
        closest_enemy = None
        closest_distance = float('inf')
        
        for unit in units:
            if unit.team != self.team and unit.hp > 0:
                distance = self.distance_to(unit)
                if distance < closest_distance and distance < 300:  # Видимость ограничена
                    closest_distance = distance
                    closest_enemy = unit
                    
        self.target_enemy = closest_enemy
        
    def attack(self, enemy):
        if self.attack_timer <= 0:
            enemy.take_damage(self.damage)
            self.attack_timer = self.attack_cooldown
            
            # Эффект атаки
            if self.unit_type == UnitType.ARCHER:
                # Стрела
                return Projectile(self.x, self.y, enemy.x, enemy.y, self.damage, self.team)
        return None
        
    def take_damage(self, damage):
        self.hp -= damage
        self.hp = max(0, self.hp)
        
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx*dx + dy*dy)
        
    def resolve_collisions(self, units):
        for unit in units:
            if unit != self and unit.hp > 0 and unit.team == self.team:  # Только союзники толкаются
                dx = unit.x - self.x
                dy = unit.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                min_distance = self.radius + unit.radius + 3  # +3 для небольшого зазора
                
                if distance < min_distance and distance > 0:
                    # Отталкивание
                    overlap = min_distance - distance
                    move_x = (dx / distance) * overlap * 0.5
                    move_y = (dy / distance) * overlap * 0.5
                    
                    self.x -= move_x
                    self.y -= move_y
                    unit.x += move_x
                    unit.y += move_y
                    
    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y
        self.target_enemy = None
        
    def is_clicked(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return dx*dx + dy*dy <= self.radius*self.radius

class Projectile:
    def __init__(self, x, y, target_x, target_y, damage, team):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.damage = damage
        self.team = team
        self.speed = 8
        self.radius = 3
        self.active = True
        self.color = YELLOW if team == 1 else ORANGE
        
        # Расчет направления
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            self.dx = dx / distance * self.speed
            self.dy = dy / distance * self.speed
        else:
            self.dx = 0
            self.dy = 0
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
        # Проверка выхода за пределы экрана
        if (self.x < -100 or self.x > SCREEN_WIDTH + 100 or 
            self.y < -100 or self.y > SCREEN_HEIGHT + 100):
            self.active = False
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 1)
        
    def check_hit(self, units):
        for unit in units:
            if unit.team != self.team and unit.hp > 0:
                dx = unit.x - self.x
                dy = unit.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < unit.radius:
                    unit.take_damage(self.damage)
                    self.active = False
                    return True
        return False

class WaveManager:
    def __init__(self):
        self.wave_number = 0
        self.wave_timer = 0
        self.wave_interval = WAVE_INTERVAL * FPS  # Конвертируем в кадры
        self.enemies_in_wave = 3
        self.wave_active = False
        
    def update(self):
        self.wave_timer += 1
        if self.wave_timer >= self.wave_interval:
            self.wave_timer = 0
            self.wave_number += 1
            self.wave_active = True
            # Увеличиваем сложность с каждой волной
            self.enemies_in_wave = 3 + self.wave_number * 2
            
    def spawn_wave(self, units):
        if not self.wave_active:
            return []
            
        new_enemies = []
        wave_enemies = self.enemies_in_wave
        
        # Распределение типов юнитов в волне
        for i in range(wave_enemies):
            # Тип юнита зависит от номера волны
            if self.wave_number < 2:
                unit_type = UnitType.WARRIOR
            elif self.wave_number < 4:
                unit_type = random.choice([UnitType.WARRIOR, UnitType.ARCHER])
            else:
                unit_type = random.choice([UnitType.WARRIOR, UnitType.ARCHER, UnitType.TANK])
            
            # Спавн с краю экрана
            side = random.randint(0, 3)
            if side == 0:  # Сверху
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = -30
            elif side == 1:  # Справа
                x = SCREEN_WIDTH + 30
                y = random.randint(50, SCREEN_HEIGHT - 150)
            elif side == 2:  # Снизу
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = SCREEN_HEIGHT - 50
            else:  # Слева
                x = -30
                y = random.randint(50, SCREEN_HEIGHT - 150)
            
            # Цвет врага
            if unit_type == UnitType.WARRIOR:
                color = DARK_RED
            elif unit_type == UnitType.ARCHER:
                color = ORANGE
            else:
                color = BROWN
                
            enemy = Unit(x, y, color, 2, unit_type)
            
            # Начальная цель врага - центр базы игрока
            enemy.target_x = SCREEN_WIDTH // 2
            enemy.target_y = 100
            
            new_enemies.append(enemy)
            
        self.wave_active = False
        return new_enemies
        
    def get_time_until_next_wave(self):
        seconds_left = (self.wave_interval - self.wave_timer) // FPS
        return max(0, seconds_left)
        
    def draw(self, screen, font, small_font):
        # Панель волн
        wave_panel = pygame.Rect(SCREEN_WIDTH - 250, 10, 240, 80)
        pygame.draw.rect(screen, (50, 50, 80, 180), wave_panel, border_radius=10)
        pygame.draw.rect(screen, WHITE, wave_panel, 2, border_radius=10)
        
        wave_text = font.render(f"Волна: {self.wave_number}", True, YELLOW)
        screen.blit(wave_text, (SCREEN_WIDTH - 240, 20))
        
        time_left = self.get_time_until_next_wave()
        time_text = small_font.render(f"След. волна: {time_left}с", True, GREEN if time_left > 10 else ORANGE if time_left > 5 else RED)
        screen.blit(time_text, (SCREEN_WIDTH - 240, 55))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Стратегия с волнами врагов")
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        # Кнопки меню
        self.start_button = Button(400, 200, 200, 50, "Начать игру")
        self.quit_button = Button(400, 300, 200, 50, "Выйти")
        
        # Кнопки создания юнитов
        self.warrior_button = Button(20, SCREEN_HEIGHT - 80, 120, 50, "Воин")
        self.archer_button = Button(150, SCREEN_HEIGHT - 80, 120, 50, "Лучник")
        self.tank_button = Button(280, SCREEN_HEIGHT - 80, 120, 50, "Танк")
        
        # Игровые объекты
        self.units = []
        self.selected_units = []
        self.projectiles = []
        self.drag_start = None
        self.drag_rect = None
        self.resources = 500
        self.unit_costs = {
            UnitType.WARRIOR: 100,
            UnitType.ARCHER: 150,
            UnitType.TANK: 250
        }
        
        # Менеджер волн
        self.wave_manager = WaveManager()
        
        # Создаем начальных юнитов игрока
        self.create_initial_units()
        
    def create_initial_units(self):
        # База игрока
        base_x, base_y = SCREEN_WIDTH // 2, 100
        
        # Несколько начальных юнитов игрока
        for i in range(3):
            unit = Unit(
                base_x - 50 + i * 50, 
                base_y + 50, 
                BLUE, 
                1, 
                UnitType.WARRIOR
            )
            self.units.append(unit)
            
        # Один лучник для защиты
        archer = Unit(base_x, base_y + 100, GREEN, 1, UnitType.ARCHER)
        self.units.append(archer)
                
    def handle_menu_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.is_hovered(mouse_pos)
        
        if self.start_button.is_clicked(mouse_pos, event):
            self.state = "game"
            
        if self.quit_button.is_clicked(mouse_pos, event):
            pygame.quit()
            sys.exit()
            
    def handle_game_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        # Кнопки создания юнитов
        self.warrior_button.is_hovered(mouse_pos)
        self.archer_button.is_hovered(mouse_pos)
        self.tank_button.is_hovered(mouse_pos)
        
        if self.warrior_button.is_clicked(mouse_pos, event):
            self.create_unit_at_spawn(UnitType.WARRIOR)
        elif self.archer_button.is_clicked(mouse_pos, event):
            self.create_unit_at_spawn(UnitType.ARCHER)
        elif self.tank_button.is_clicked(mouse_pos, event):
            self.create_unit_at_spawn(UnitType.TANK)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                # Проверяем, кликнули ли по юниту
                unit_clicked = False
                for unit in self.units:
                    if unit.team == 1 and unit.is_clicked(mouse_pos):
                        unit_clicked = True
                        if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self.selected_units = []
                            for u in self.units:
                                u.selected = False
                        unit.selected = True
                        if unit not in self.selected_units:
                            self.selected_units.append(unit)
                        break
                        
                # Если не кликнули по юниту - начинаем выделение рамкой
                if not unit_clicked:
                    self.drag_start = mouse_pos
                    if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.selected_units = []
                        for unit in self.units:
                            unit.selected = False
                            
            elif event.button == 3:  # Правая кнопка мыши
                # Проверяем, кликнули ли по вражескому юниту
                enemy_clicked = False
                for unit in self.units:
                    if unit.team != 1 and unit.is_clicked(mouse_pos) and unit.hp > 0:
                        enemy_clicked = True
                        for selected in self.selected_units:
                            selected.target_enemy = unit
                        break
                        
                # Если кликнули по земле - перемещение
                if not enemy_clicked:
                    for unit in self.selected_units:
                        unit.set_target(mouse_pos[0], mouse_pos[1])
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.drag_start:
                self.select_units_in_rect()
                self.drag_start = None
                self.drag_rect = None
                
        elif event.type == pygame.MOUSEMOTION:
            if self.drag_start:
                x1, y1 = self.drag_start
                x2, y2 = mouse_pos
                self.drag_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "menu"
            elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+A - выбрать все живые юниты игрока
                self.selected_units = [unit for unit in self.units if unit.team == 1 and unit.hp > 0]
                for unit in self.units:
                    unit.selected = (unit in self.selected_units)
                    
    def create_unit_at_spawn(self, unit_type):
        if self.resources >= self.unit_costs[unit_type]:
            # Спавним юнита возле базы
            spawn_x = SCREEN_WIDTH // 2 + random.randint(-80, 80)
            spawn_y = 100 + random.randint(0, 50)
            
            color = BLUE if unit_type == UnitType.WARRIOR else GREEN if unit_type == UnitType.ARCHER else PURPLE
            unit = Unit(spawn_x, spawn_y, color, 1, unit_type)
            self.units.append(unit)
            self.resources -= self.unit_costs[unit_type]
            
    def select_units_in_rect(self):
        if not self.drag_rect:
            return
            
        for unit in self.units:
            if unit.hp > 0 and unit.team == 1 and self.drag_rect.collidepoint(unit.x, unit.y):
                unit.selected = True
                if unit not in self.selected_units:
                    self.selected_units.append(unit)
                    
    def update_game(self):
        # Обновляем менеджер волн
        self.wave_manager.update()
        
        # Спавним новую волну если пришло время
        new_enemies = self.wave_manager.spawn_wave(self.units)
        self.units.extend(new_enemies)
        
        # Удаляем мертвых юнитов
        dead_units = [unit for unit in self.units if unit.hp <= 0]
        for unit in dead_units:
            if unit in self.selected_units:
                self.selected_units.remove(unit)
            # При смерти врага добавляем ресурсы
            if unit.team == 2:
                self.resources += 50 + self.wave_manager.wave_number * 10  # Больше ресурсов за волны
        self.units = [unit for unit in self.units if unit.hp > 0]
        
        # Обновляем юнитов
        for unit in self.units:
            projectile = unit.update(self.units)
            if projectile:
                self.projectiles.append(projectile)
                
        # Обновляем снаряды
        for projectile in self.projectiles[:]:
            projectile.update()
            projectile.check_hit(self.units)
            if not projectile.active:
                self.projectiles.remove(projectile)
                
        # Автоматически добавляем ресурсы (медленный прирост)
        if random.random() < 0.01:  # 1% шанс каждый кадр
            self.resources += 5
            
    def draw_menu(self):
        self.screen.fill(LIGHT_BLUE)
        
        title = self.font.render("Стратегия с волнами", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        
        # Инструкция
        instructions = [
            "Враги атакуют волнами каждые 30 секунд!",
            "Управление:",
            "ЛКМ - выделить юнита/выделить область",
            "ПКМ по земле - переместить",
            "ПКМ по врагу - атаковать",
            "Shift+ЛКМ - добавить к выделению",
            "Ctrl+A - выделить всех своих юнитов",
            "ESC - главное меню"
        ]
        
        for i, line in enumerate(instructions):
            text = self.small_font.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - 300, 400 + i * 30))
            
    def draw_game(self):
        # Фон
        self.screen.fill(DARK_GREEN)
        
        # Рисуем базу игрока
        base_x, base_y = SCREEN_WIDTH // 2, 100
        pygame.draw.circle(self.screen, (100, 100, 255), (base_x, base_y), 40)
        pygame.draw.circle(self.screen, WHITE, (base_x, base_y), 40, 3)
        base_text = self.small_font.render("База", True, WHITE)
        self.screen.blit(base_text, (base_x - 25, base_y - 10))
        
        # Рисуем сетку
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, (40, 70, 40), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, (40, 70, 40), (0, y), (SCREEN_WIDTH, y), 1)
            
        # Рисуем снаряды
        for projectile in self.projectiles:
            projectile.draw(self.screen)
            
        # Рисуем юнитов
        for unit in self.units:
            unit.draw(self.screen)
            
        # Рисуем рамку выделения
        if self.drag_rect:
            pygame.draw.rect(self.screen, BLUE, self.drag_rect, 2)
            
        # Рисуем панель волн
        self.wave_manager.draw(self.screen, self.font, self.small_font)
            
        # Нижняя панель интерфейса
        info_panel = pygame.Rect(0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120)
        pygame.draw.rect(self.screen, (50, 50, 80, 230), info_panel)
        pygame.draw.line(self.screen, WHITE, (0, SCREEN_HEIGHT - 120), (SCREEN_WIDTH, SCREEN_HEIGHT - 120), 3)
        
        # Ресурсы
        resources_text = self.font.render(f"Ресурсы: {self.resources}", True, YELLOW)
        self.screen.blit(resources_text, (20, SCREEN_HEIGHT - 110))
        
        # Статистика
        player_units = len([u for u in self.units if u.team == 1])
        enemy_units = len([u for u in self.units if u.team == 2])
        stats_text = self.small_font.render(f"Союзников: {player_units}  Врагов: {enemy_units}", True, WHITE)
        self.screen.blit(stats_text, (20, SCREEN_HEIGHT - 70))
        
        # Кнопки создания юнитов
        self.warrior_button.draw(self.screen)
        self.archer_button.draw(self.screen)
        self.tank_button.draw(self.screen)
        
        # Цены юнитов
        warrior_cost = self.small_font.render(f"{self.unit_costs[UnitType.WARRIOR]}", True, YELLOW)
        archer_cost = self.small_font.render(f"{self.unit_costs[UnitType.ARCHER]}", True, YELLOW)
        tank_cost = self.small_font.render(f"{self.unit_costs[UnitType.TANK]}", True, YELLOW)
        
        self.screen.blit(warrior_cost, (70, SCREEN_HEIGHT - 35))
        self.screen.blit(archer_cost, (200, SCREEN_HEIGHT - 35))
        self.screen.blit(tank_cost, (330, SCREEN_HEIGHT - 35))
        
        # Подсказка в игре
        help_text = self.small_font.render("ESC - меню | Выбрано: " + str(len(self.selected_units)), True, WHITE)
        self.screen.blit(help_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 110))
        
        # Индикация следующей волны (если скоро)
        time_left = self.wave_manager.get_time_until_next_wave()
        if time_left < 10:
            warning_text = self.small_font.render(f"Волна через {time_left} секунд!", True, RED)
            self.screen.blit(warning_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 70))
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if self.state == "menu":
                    self.handle_menu_events(event)
                elif self.state == "game":
                    self.handle_game_events(event)
                    
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "game":
                self.update_game()
                self.draw_game()
                
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()