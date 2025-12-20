import pygame 

pygame.init()

weight = 800
height = 600

screen = pygame.display.set_mode((weight,height))
pygame.display.set_caption("cтрат")

GREENSVET = (100, 255, 100)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


font = pygame.font.SysFont(None,76)
font1 = pygame.font.SysFont(None,36)

# Кнопка "Начать"
start_buton = pygame.Rect(300, 250, 200, 50)
start_color = GREEN
start_text = font1.render("Начать", True, WHITE)
start_textren = start_text.get_rect(center=start_buton.center)

exit_buton = pygame.Rect(300, 350, 200, 50)
exit_color = ((178, 34, 34))
exit_text = font1.render("Выход", True, (255, 228, 225))
exit_textren = exit_text.get_rect(center=exit_buton.center)


game_started = False


text_surface = font.render("Статегия", True, (255, 228, 225))
text_rect = text_surface.get_rect(center=(400,80))


Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        if event.type == pygame.MOUSEMOTION:
            if not game_started:
                if start_buton.collidepoint(event.pos):
                    start_color = ((0, 250, 154))
                else:
                    start_color = GREEN

        if event.type == pygame.MOUSEMOTION:
            if not game_started:
                if exit_buton.collidepoint(event.pos):
                    exit_color = ((139, 0, 0))
                else:
                    exit_color = ((178, 34, 34))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not game_started:
                    if start_buton.collidepoint(event.pos):
                        game_started = True
                        print("старт")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not game_started:
                    if exit_buton.collidepoint(event.pos):
                        Running = False
                        


    if game_started:
        screen.fill((0,0,0))
    else: 
        screen.fill((40, 40, 41))
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, start_color, start_buton)
        screen.blit(start_text,start_textren)
        pygame.draw.rect(screen, exit_color, exit_buton)
        screen.blit(exit_text,exit_textren)
    pygame.display.flip()

pygame.quit()