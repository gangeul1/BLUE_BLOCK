import pygame
pygame.init
pygame.font.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

myFont = pygame.font.SysFont(None, 70)

def text_printing(contents,x,y,color):
    text = myFont.render(f"{contents}" , True, (color))
    screen.blit(text, (x,y))