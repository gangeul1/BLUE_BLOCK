import pygame
import os

pygame.init
script_dir = os.path.dirname(__file__)

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

click = False


class button:
    def __init__(self,sx,sy,image_name,image_name2):
        self.image_name = f"{script_dir}//images//{image_name}"
        self.image_name2 = f"{script_dir}//images//{image_name2}"
        self.real_image = self.image_name
        self.image = pygame.image.load(self.image_name)
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.sx = sx
        self.sy = sy
        self.fx = self.sx + self.width
        self.fy = self.sy + self.height
        self.last_click = 0


    def button_work(self,click):
        pos = pygame.mouse.get_pos()
        if self.sx < pos[0] < self.fx and self.sy < pos[1] < self.fy:
            self.real_image = self.image_name2
            screen.blit(pygame.image.load(self.real_image),(self.sx,self.sy))
            if click == True:
                return True
            else:
                return False
        else:
            self.real_image = self.image_name
            screen.blit(pygame.image.load(self.real_image),(self.sx,self.sy))
            return False
        
        