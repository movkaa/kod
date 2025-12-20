import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("супер кликер расширение")

# Цвета
COLOR_BACKGROUND = (0, 0, 0)
COLOR_COOKIE = (255, 106, 0)
COLOR_TEXT = (255, 100, 100)
COLOR_UPGRADE = (99, 95, 92)
COLOR_AUTO_UPGRADE = (0, 128, 0)
COLOR_PROGRESS = (255, 255, 0)
COLOR_EFFECT = (255, 255, 255)

# Области
cookie_radius = 80
cookie_rect = pygame.Rect(
    WIDTH // 2 - cookie_radius,
    HEIGHT // 2 - cookie_radius,
    cookie_radius * 2,
    cookie_radius * 2
)

buy_upgrade_rect = pygame.Rect(600, 10, 150, 50)
Щ_rect = pygame.Rect(600, 70, 150, 50)

# Эффекты клика
click_effects = []

# Состояние игры
try:
    with open("text.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
        kliki = int(lines[0])
        kolup = int(lines[1])
        sherk = int(lines[2])
        achievements = set(lines[3:])
except:
    kliki = 0
    kolup = 0
    sherk = 1
    achievements = set()

# Настройка FPS
clock = pygame.time.Clock()
FPS = 60

# Достижения
ACHIEVEMENTS = {
    "First 1000": {"condition": lambda: kliki >= 1000, "unlocked": False},
    "Level 5": {"condition": lambda: kolup >= 5, "unlocked": False},
}

def save_game():
    """Сохраняет состояние игры в файл."""
    with open("text.txt", "w", encoding="utf-8") as f:
        f.write(f"{int(kliki)}\n{kolup}\n{sherk}\n")
        f.write("\n".join(achievements))

def draw():
    """Отрисовка элементов."""
    screen.fill(COLOR_BACKGROUND)
    # Область апгрейда
    pygame.draw.rect(screen, COLOR_UPGRADE, buy_upgrade_rect)
    pygame.draw.rect(screen, COLOR_UPGRADE, Щ_rect)
    # Печенька
    pygame.draw.circle(screen, COLOR_COOKIE, (WIDTH // 2, HEIGHT // 2), cookie_radius)
    # Текст
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(f"Клики: {int(kliki)}", True, COLOR_TEXT)
    screen.blit(text_surface, (10, 10))
    level_text = font.render(f"Уровень апгрейда: {kolup}", True, COLOR_TEXT)
    screen.blit(level_text, (510, 60))
    # Надписи для кнопок
    font_button = pygame.font.SysFont(None, 20)
    screen.blit(font_button.render("Купить апгрейд (100)", True, (255,255,255)), (buy_upgrade_rect.x + 5, buy_upgrade_rect.y + 15))
    screen.blit(font_button.render("Купить шреков (500)", True, (255,255,255)), (Щ_rect.x + 5, Щ_rect.y + 15))
    # Эффекты клика
    for effect in click_effects:
        pygame.draw.circle(screen, effect['color'], effect['pos'], effect['radius'])
    # Достижения
    y_offset = 200
    for name, data in ACHIEVEMENTS.items():
        status = "+" if data["condition"]() else "-"
        achievement_text = font.render(f"{status} {name}", True, COLOR_TEXT)
        screen.blit(achievement_text, (10, y_offset))
        y_offset += 30
    pygame.display.flip()

def handle_click(pos):
    """Обработка кликов."""
    global kliki, kolup, auto_clickers, achievements, sherk
    if cookie_rect.collidepoint(pos):
        kliki += 1 * sherk
        # Эффект
        click_effects.append({'pos': pos, 'radius': 10, 'color': COLOR_EFFECT})
    elif buy_upgrade_rect.collidepoint(pos):
        if kliki >= 100:
            kliki -= 100
            kolup += 1
    elif Щ_rect.collidepoint(pos):
        if kliki >= 500:
            kliki -= 500
            sherk += 1

def check_achievements():
    """Проверка и разблокировка достижений."""
    global achievements
    for name, data in ACHIEVEMENTS.items():
        if name not in achievements and data["condition"]():
            achievements.add(name)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

    kliki += kolup * (1 / FPS)

    # Обновление эффектов
    for effect in click_effects:
        effect['radius'] += 1
    click_effects = [e for e in click_effects if e['radius'] < 30]

    # Проверка достижений
    check_achievements()

    # Отрисовка
    draw()
    clock.tick(FPS)

# Сохранение
save_game()
pygame.quit()