import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размер окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бесконечный кликер")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
RED = (220, 20, 60)

# Шрифты
font_large = pygame.font.SysFont('Arial', 36)
font_medium = pygame.font.SysFont('Arial', 28)

# Переменные
total_clicks = 0
session_clicks = 0
clicks_per_click = 1

# Кнопки
buttons = {
    'Click': pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 60),
    'Reset': pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 80, 100, 40),
    'Exit': pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 130, 100, 40),
    'Increase': pygame.Rect(50, HEIGHT - 100, 150, 40),
    'Decrease': pygame.Rect(220, HEIGHT - 100, 150, 40),
    'Max': pygame.Rect(390, HEIGHT - 100, 150, 40),
    'Min': pygame.Rect(560, HEIGHT - 100, 150, 40)
}

# Основной цикл
running = True
while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Проверка кнопки "Клик"
            if buttons['Click'].collidepoint(mouse_x, mouse_y):
                total_clicks += clicks_per_click
                session_clicks += clicks_per_click
            # Проверка других кнопок
            elif buttons['Reset'].collidepoint(mouse_x, mouse_y):
                total_clicks = 0
                session_clicks = 0
            elif buttons['Exit'].collidepoint(mouse_x, mouse_y):
                running = False
            elif buttons['Increase'].collidepoint(mouse_x, mouse_y):
                clicks_per_click += 1
            elif buttons['Decrease'].collidepoint(mouse_x, mouse_y):
                if clicks_per_click > 1:
                    clicks_per_click -= 1
            elif buttons['Max'].collidepoint(mouse_x, mouse_y):
                clicks_per_click = 50
            elif buttons['Min'].collidepoint(mouse_x, mouse_y):
                clicks_per_click = 1

    # Отрисовка текста счетчиков
    total_text = font_large.render(f"Общее число кликов: {total_clicks}", True, BLACK)
    session_text = font_medium.render(f"Кликов за сессию: {session_clicks}", True, BLACK)
    per_click_text = font_medium.render(f"Кликов за клик: {clicks_per_click}", True, BLACK)

    total_rect = total_text.get_rect(center=(WIDTH//2, 50))
    session_rect = session_text.get_rect(center=(WIDTH//2, 100))
    per_click_rect = per_click_text.get_rect(center=(WIDTH//2, 140))
    screen.blit(total_text, total_rect)
    screen.blit(session_text, session_rect)
    screen.blit(per_click_text, per_click_rect)

    # Отрисовка кнопок
    for key, rect in buttons.items():
        if key == 'Click':
            color = BLUE
        elif key == 'Reset':
            color = GREEN
        elif key == 'Exit':
            color = RED
        elif key in ('Increase', 'Max'):
            color = (255, 165, 0)
        elif key in ('Decrease', 'Min'):
            color = (255, 215, 0)
        pygame.draw.rect(screen, color, rect)
        label = font_medium.render(key, True, WHITE)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    # Обновление экрана
    pygame.display.flip()

pygame.quit()
sys.exit()