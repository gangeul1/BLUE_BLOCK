import pygame
import text_print

pygame.init()
pygame.font.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
Button_color = (0,0,0)
click = False
class button:
    def __init__(self,sx,sy,fx,fy,out_put):
        self.sx = sx
        self.sy = sy
        self.fx = fx-sx
        self.fy = fy-sy
        self.out_put = out_put 

    def button(self,period):
        global Button_color
        pos = pygame.mouse.get_pos()
        if self.sx-30 < pos[0] < self.fx + self.sx+period and self.sy-period < pos[1] < self.fy + self.sy + period:
            Button_color = (80,80,80)
            if click == True:
                self.out_put = True
        else:
            Button_color = (0,0,0)
        pygame.draw.rect(screen, (255,255,255), [self.sx-period,self.sy-period,self.fx+period*2,self.fy+period*2])
        pygame.draw.rect(screen, (Button_color), [self.sx,self.sy,self.fx,self.fy])
    
game_start_button = button(200,370,600,440,False)
option_button = button(200,510,600,580,False)
quit_button = button(200,650,600,720,False)



def game_manu():
    global running, click
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        
    pygame.draw.rect(screen, (50,50,50), [0,0, screen_width,screen_height])
    
    game_start_button.button(10)
    option_button.button(10)
    quit_button.button(10)
    text_print.text_printing("THE BLUE BLOCK",100,180,(255,255,255),None,97)
    text_print.text_printing("GAME START",screen_width/2 - 135,388,(255,255,255),None,60)
    text_print.text_printing("QUIT",screen_width/2 - 50,668,(255,255,255),None,60)
    if game_start_button.out_put == True:
        return "game_playing"
    elif option_button.out_put == True:
        return "manu" # 임시
    elif quit_button.out_put == True:
        return "quit"
    else:
        pygame.display.flip()
        return "manu"
