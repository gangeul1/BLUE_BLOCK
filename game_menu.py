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




start_button = button.button(720,400,"button.png","button2.png")
stage_button = button.button(720,510,"button.png","button2.png")
quit2_button = button.button(720,620,"button.png","button2.png")

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
    elif quit2_button.button_work(click) == True:
        result = "quit"
    else:
        result = "menu"
    text_print.text_printing("GAME START",795,427,(255,255,255),None,60)
    text_print.text_printing("STAGE",795 + 65,537,(255,255,255),None,60)
    text_print.text_printing("QUIT",795 + 85,647,(255,255,255),None,60)
    pygame.display.flip()
    return result



game_continue_button = button.button(screen_width/2-210,160,"button.png","button2.png")
game_restart_button = button.button(screen_width/2-210,300,"button.png","button2.png")
menu_button = button.button(screen_width/2-210,440,"button.png","button2.png")
quit1_button = button.button(screen_width/2-210,580,"button.png","button2.png")


def pause():
    global click, result
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
    elif quit1_button.button_work(click) == True:
        result = "quit"
    elif game_continue_button.button_work(click) == True:
        result = "continue"
    else:
        result = "pause"
    
    text_print.text_printing("CONTINUE",screen_width/2 - 110,188,(255,255,255),None,60)
    text_print.text_printing("RESTART",screen_width/2 - 92,328,(255,255,255),None,60)
    text_print.text_printing("MENU",screen_width/2 - 60,468,(255,255,255),None,60)
    text_print.text_printing("QUIT",screen_width/2 - 50,608,(255,255,255),None,60)

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
    global click, result
    for order in range(len(maps)):
        if maps[order] == map_file:
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
            return maps[temp], "menu"
        
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
    return map_file,game_condition