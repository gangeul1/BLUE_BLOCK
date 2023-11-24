import pygame
import text_print
import os
import button

pygame.init()
pygame.font.init()
script_dir = os.path.dirname(__file__)

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

setting = 0
temp1 = 0
temp2 = 0
click = False

start_button = button.button(820,400,"button.png","button2.png")
stage_button = button.button(820,510,"button.png","button2.png")
playmode_button = button.button(820,620,"button.png","button2.png")

def start_menu():
    global click, result
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        
    screen.blit(pygame.image.load(f"{script_dir}//images//Menu.jpg"),(0,0))
    


    if start_button.button_work(click) == True:
        result = "game_restart"
    elif stage_button.button_work(click)== True:
        result = "stage" 
    elif playmode_button.button_work(click) == True:
        result = "play_mode"
    else:
        result = "menu"
    text_print.text_printing("GAME START",895,427,(255,255,255),None,60)
    text_print.text_printing("STAGE",895 + 65,537,(255,255,255),None,60)
    text_print.text_printing("PLAY MODE",895 + 15,647,(255,255,255),None,60)
    pygame.display.flip()
    return result



game_continue_button = button.button(screen_width/2-210,130,"button.png","button2.png")
game_restart_button = button.button(screen_width/2-210,320,"button.png","button2.png")
menu_button = button.button(screen_width/2-210,510,"button.png","button2.png")


def pause():
    global click, result
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False


    if game_restart_button.button_work(click) == True:
        result = "game_restart"
    elif menu_button.button_work(click) == True:
        result = "menu" 
    elif game_continue_button.button_work(click) == True:
        result = "continue"
    else:
        result = "pause"
    
    text_print.text_printing("CONTINUE",screen_width/2 - 110,158,(255,255,255),None,60)
    text_print.text_printing("RESTART",screen_width/2 - 92,348,(255,255,255),None,60)
    text_print.text_printing("MENU",screen_width/2 - 60,538,(255,255,255),None,60)

    pygame.display.flip()
    return result

temp = -1
temp2 = 1
map_buttons = []
maps = os.listdir(f"{script_dir}//maps")
for order in range(len(maps)):
    temp = order % 5
    temp2 = order/5 - order/5%1 + 0.5
    map_buttons.append(button.button(temp * 256 + 29,240 * temp2 ,"stage_box.png","stage_box2.png"))

quit3_button = button.button(10,10,"quit_button.png","quit_button2.png")

def stage(map_file):
    global click
    click = False
    for order in range(len(maps)):
        if maps[order] == map_file:
            stage_count = order
            map_buttons[order].image_name = f"{script_dir}//images//selected_stage_box.png"
            map_buttons[order].image_name2 = f"{script_dir}//images//selected_stage_box2.png"
        else:
            map_buttons[order].image_name = f"{script_dir}//images//stage_box.png"
            map_buttons[order].image_name2 = f"{script_dir}//images//stage_box2.png"

    pygame.draw.rect(screen, (0,0,0), [0,0, screen_width,screen_height])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "a","quit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
    

    temp = -1
    for map_button in map_buttons:
        temp += 1
        if map_button.button_work(click) == True:
            return maps[temp], "menu",temp
        
    if quit3_button.button_work(click) == True:
        game_condition = "menu"
    else:
        game_condition = "stage"
    text_print.text_printing("MENU",33,35,(255,255,255),None,60)

    temp = -1
    temp2 = 1
    for order in range(len(maps)):
        temp = order % 5
        temp2 = order/5 - order/5%1 + 0.5
        text_print.text_printing(f"{order+1}",temp * 256 +100,240 * temp2+ 60,(255,255,255),None,150)

    pygame.display.flip()
    return [map_file,game_condition,stage_count]

left_arrow_button = button.button(300,580,"left_arrow1.png","left_arrow2.png")
right_arrow_button = button.button(920,580,"right_arrow1.png","right_arrow2.png")
select_button = button.button(screen_width/2 -210,620,"button.png","button2.png")

def play_mode():
    global click,temp1,temp2, setting,result
    pygame.draw.rect(screen, (0,0,0), [0,0, screen_width,screen_height])
    screen.blit(pygame.image.load(f"{script_dir}\images//setting{setting}.png"),(screen_width/2-220,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit",setting
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            click = False
    if left_arrow_button.button_work(click) == True:
        result = "play_mode"
        if setting > 0:
            setting -= temp1
        else:
            if temp1 != 0:
                setting = 5
        temp1 = 0
    elif right_arrow_button.button_work(click) == True:
        result = "play_mode"
        if setting < 5:
            setting += temp2
        else:
            if temp2 != 0:
                setting = 0
        temp2 = 0
    else:
        result = "play_mode"
        temp1 = 1
        temp2 = 1
    if select_button.button_work(click) == True:
        result = "menu"
    

    text_print.text_printing("SELECT",screen_width/2 -80,645,(255,255,255),None,60)
    if setting == 4:
        text_print.text_printing("In this mode, you can't earn the points.",screen_width/2-120,screen_height-160,(255,0,0),None,20)
    pygame.display.flip()

    return result, setting
    