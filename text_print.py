import pygame
pygame.init
pygame.font.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))


def text_printing(contents,x,y,color,font = None, size = 70):
    text = pygame.font.SysFont(font, size).render(f"{contents}" , True, (color))
    screen.blit(text, (x,y))