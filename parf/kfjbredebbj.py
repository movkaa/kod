import pygame
import time

pygame.init()
widght = 800
height = 600
screen = pygame.display.set_mode((widght,height))
pygame.display.set_caption("супер кликер")

with open ("text.txt","r",encoding="utf-8") as f:
    a = f.read()

kolup = 0
fon = (0,0,0)
cookie = (255, 106, 0)
texte = (255,100,100)
kliki = int(a)
cokrad = 80
upgrade = (99, 95, 92)
upbody = pygame.Rect((600,10, 150,100))
cokbody = pygame.Rect(widght//2 - cokrad//2, height//2 - cokrad//2, cokrad, cokrad)
Running = True
upgradeqwe = (100,150)

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            with open("text.txt", "w", encoding="utf-8") as f:
                    f.write(f"{kliki}\n{kolup}")
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if cokbody.collidepoint(mouse_pos):
                kliki +=1000
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if upbody.collidepoint(mouse_pos):
                if kliki >= 100:
                    kliki -= 100
                    kolup += 1
                    
                
    time.sleep(0.3)
    kliki += 1 * kolup

    screen.fill(fon)
    pygame.draw.rect(screen,upgrade,(600,10, 150,100))
    pygame.draw.circle(screen,cookie, (400, 300), cokrad)
    font = pygame.font.SysFont(None,36)
    text = font.render(f"Клики: {kliki}", True, texte)
    screen.blit(text,(10,10))
    pygame.display.flip()
pygame.quit()




