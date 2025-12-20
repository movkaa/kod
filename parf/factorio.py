import pygame
import sys
import random

pygame.init()

# Размеры мира и окна
WORLD_SIZE = 200
CELL_SIZE = 32
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
UI_HEIGHT = 150

# Создаем окно
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Игровое поле с построениями и ресурсами")

font = pygame.font.SysFont("Arial", 16)

# Цвета
BG_COLOR = (20, 20, 20)
GRID_COLOR = (50, 50, 50)
RESOURCE_COLOR = (200, 150, 50)
PLAYER_COLOR = (0, 255, 0)
BUILD_COLORS = [
    (255, 100, 100),
    (255, 255, 100),
    (100, 255, 255),
    (255, 100, 255),
    (150, 75, 0),
    (100, 100, 100),
    (255, 165, 0),
    (138, 43, 226),
    (0, 255, 127),
    (255, 215, 0),
]

# Объекты
resources = 0
player_pos = [WORLD_SIZE // 2, WORLD_SIZE // 2]
camera_x = 0
camera_y = 0
camera_speed = 0.1

# Создаем мир
grid = [[{'resource': False, 'structure': None, 'structure_type': None} for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
for _ in range(3000):
    x = random.randint(0, WORLD_SIZE - 1)
    y = random.randint(0, WORLD_SIZE - 1)
    grid[y][x]['resource'] = True

# Постройки с функциями и эффектами
buildings = [
    {
        'name': 'Комбинат', 
        'cost': 20, 
        'description': 'Обрабатывает ресурсы для производства товаров.', 
        'effect': 'produce_resources', 
        'effect_value': 1
    },
    {
        'name': 'Электростанция', 
        'cost': 15, 
        'description': 'Производит электроэнергию.', 
        'effect': 'produce_energy', 
        'effect_value': 1
    },
    {
        'name': 'Лагерь', 
        'cost': 10, 
        'description': 'Обеспечивает укрытие и хранение ресурсов.', 
        'effect': 'storage', 
        'effect_value': 50
    },
    {
        'name': 'Учреждение', 
        'cost': 25, 
        'description': 'Образовательное и исследовательское учреждение.', 
        'effect': 'research', 
        'effect_value': 1
    },
    {
        'name': 'Научный центр', 
        'cost': 30, 
        'description': 'Разрабатывает новые технологии.', 
        'effect': 'tech_development', 
        'effect_value': 1
    },
    {
        'name': 'Хранилище', 
        'cost': 10, 
        'description': 'Хранит ресурсы и товары.', 
        'effect': 'storage_increase', 
        'effect_value': 100
    },
    {
        'name': 'Ферма', 
        'cost': 12, 
        'description': 'Производит продукты питания.', 
        'effect': 'produce_food', 
        'effect_value': 1
    },
    {
        'name': 'Ремонтка', 
        'cost': 20, 
        'description': 'Ремонтирует оборудование.', 
        'effect': 'repair', 
        'effect_value': 1
    },
    {
        'name': 'Маяк', 
        'cost': 18, 
        'description': 'Обеспечивает навигацию и безопасность.', 
        'effect': 'navigation', 
        'effect_value': 1
    },
    {
        'name': 'Лаборатория', 
        'cost': 35, 
        'description': 'Исследовательский центр.', 
        'effect': 'research_speed', 
        'effect_value': 1
    },
]

show_build_menu = False
selected_building_index = 0

# Эффекты игрока и мира
player_effects = {
    'produce_resources': 1,
    'produce_food': 1,
    'storage': 100,
    'energy': 0,
    'research': 0,
    'tech_development': 0,
    'navigation': 0,
    'research_speed': 1,
    'speed_multiplier': 1,
}

clock = pygame.time.Clock()

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                show_build_menu = not show_build_menu
            elif event.key == pygame.K_e:
                # Собрать ресурс
                x, y = player_pos
                if 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE:
                    cell = grid[y][x]
                    if cell['resource']:
                        resources += 1 * player_effects.get('produce_resources', 1)
                        cell['resource'] = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if player_pos[0] < WORLD_SIZE - 1:
                    player_pos[0] += 1
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if player_pos[0] > 0:
                    player_pos[0] -= 1
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if player_pos[1] > 0:
                    player_pos[1] -= 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if player_pos[1] < WORLD_SIZE - 1:
                    player_pos[1] += 1
            elif show_build_menu and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                                    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                index = event.key - pygame.K_1
                if index >= 0 and index < len(buildings):
                    b = buildings[index]
                    # размещение рядом
                    nx, ny = player_pos
                    placed = False
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx2 = nx + dx
                            ny2 = ny + dy
                            if 0 <= nx2 < WORLD_SIZE and 0 <= ny2 < WORLD_SIZE:
                                cell = grid[ny2][nx2]
                                if cell['structure'] is None and (nx2, ny2) != tuple(player_pos):
                                    if resources >= b['cost']:
                                        resources -= b['cost']
                                        cell['structure'] = index
                                        cell['structure_type'] = b
                                        # эффект
                                        effect_type = b['effect']
                                        effect_value = b['effect_value']
                                        # Обновляем эффекты в зависимости от типа
                                        if effect_type == 'produce_resources':
                                            player_effects['produce_resources'] += effect_value
                                        elif effect_type == 'produce_food':
                                            player_effects['produce_food'] += effect_value
                                        elif effect_type == 'storage':
                                            player_effects['storage'] += effect_value
                                        elif effect_type == 'navigation':
                                            player_effects['speed_multiplier'] += effect_value * 0.1
                                        elif effect_type == 'research_speed':
                                            player_effects['research_speed'] += effect_value
                                        # Можно добавить для других эффектов
                                    placed = True
                                    break
                        if placed:
                            break
                    show_build_menu = False

    # Обновляем скорость перемещения с учетом эффекта маяка
    move_speed = 0.1 * player_effects.get('speed_multiplier', 1)

    # Обновляем камеру
    target_x = player_pos[0] * CELL_SIZE + CELL_SIZE // 2 - WINDOW_WIDTH // 2
    target_y = player_pos[1] * CELL_SIZE + CELL_SIZE // 2 - (WINDOW_HEIGHT - UI_HEIGHT) // 2
    camera_x += (target_x - camera_x) * camera_speed
    camera_y += (target_y - camera_y) * camera_speed

    # Отрисовка
    screen.fill(BG_COLOR)

    min_x = int(camera_x // CELL_SIZE)
    min_y = int(camera_y // CELL_SIZE)

    for y in range(WINDOW_HEIGHT // CELL_SIZE + 2):
        for x in range(WINDOW_WIDTH // CELL_SIZE + 2):
            world_x = min_x + x
            world_y = min_y + y
            if 0 <= world_x < WORLD_SIZE and 0 <= world_y < WORLD_SIZE:
                rect = pygame.Rect(x * CELL_SIZE - (camera_x % CELL_SIZE),
                                   y * CELL_SIZE - (camera_y % CELL_SIZE),
                                   CELL_SIZE, CELL_SIZE)
                cell = grid[world_y][world_x]
                pygame.draw.rect(screen, GRID_COLOR, rect)
                if cell['resource']:
                    pygame.draw.circle(screen, RESOURCE_COLOR, rect.center, CELL_SIZE // 3)
                if cell['structure'] is not None:
                    color = BUILD_COLORS[cell['structure']]
                    pygame.draw.rect(screen, color, rect.inflate(-2, -2))

    # Draw player
    player_screen_x = (player_pos[0] * CELL_SIZE + CELL_SIZE // 2 - camera_x)
    player_screen_y = (player_pos[1] * CELL_SIZE + CELL_SIZE // 2 - camera_y)
    pygame.draw.circle(screen, PLAYER_COLOR, (int(player_screen_x), int(player_screen_y)), CELL_SIZE // 2)

    # UI снизу
    pygame.draw.rect(screen, (30, 30, 30), (0, WINDOW_HEIGHT - UI_HEIGHT, WINDOW_WIDTH, UI_HEIGHT))
    resources_text = font.render(f"Ресурсы: {resources}", True, (255, 255, 255))
    screen.blit(resources_text, (10, WINDOW_HEIGHT - UI_HEIGHT + 10))
    instr = font.render("WASD/Стрелки - движение, 'E' - собрать, 'B' - меню, цифры - построить", True, (255, 255, 255))
    screen.blit(instr, (200, WINDOW_HEIGHT - UI_HEIGHT + 10))

    # Меню построек
    if show_build_menu:
        menu_width = len(buildings) * 120
        menu_height = 80
        menu_x = (WINDOW_WIDTH - menu_width) // 2
        menu_y = WINDOW_HEIGHT - UI_HEIGHT + 50
        # Основной фон меню
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (50, 50, 50), menu_rect)
        for i, b in enumerate(buildings):
            color = BUILD_COLORS[i]
            rect_x = menu_x + i * 120
            r = pygame.Rect(rect_x, menu_y, 120, 80)
            pygame.draw.rect(screen, color, r)
            # Название
            txt_name = font.render(f"{i+1}. {b['name']}", True, (0, 0, 0))
            screen.blit(txt_name, (r.x + 5, r.y + 5))
            # Цена
            txt_cost = font.render(f"Цена: {b['cost']}", True, (0, 0, 0))
            screen.blit(txt_cost, (r.x + 5, r.y + 25))
            # Описание
            desc = b['description']
            desc_display = desc if len(desc) <= 50 else desc[:47] + "..."
            txt_desc = font.render(desc_display, True, (0, 0, 0))
            screen.blit(txt_desc, (r.x + 5, r.y + 45))
            # Обводка выделенного
            if i == selected_building_index:
                pygame.draw.rect(screen, (255, 255, 255), r, 2)

    pygame.display.flip()
    clock.tick(60)