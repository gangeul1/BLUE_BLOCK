import os
import pygame
import map_reading
import text_print
import game_menu

pygame.init()
pygame.font.init()

script_dir = os.path.dirname(__file__)

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BLUE BLOCK")
clock = pygame.time.Clock()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
WHITE_GRAY = (100,100,100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
death_count = 0
temp = 0
temp1 = 0
temp2 = 0
#################################################################################################        

def scroll_move():
    if player.x_lot < x_scroll_period:
        for lists_name in All_Units:
            for lists_value in lists_name:
                for unit in lists_value:
                    unit.x_lot += x_scroll_period - player.x_lot
        player.x_lot = x_scroll_period
    if player.x_lot > screen_width - player.width - x_scroll_period:
        for lists_name in All_Units:
            for lists_value in lists_name:
                for unit in lists_value:
                    unit.x_lot -= player.x_lot - (screen_width - player.width - x_scroll_period)
        player.x_lot = screen_width - player.width - x_scroll_period
    if player.y_lot < y_scroll_period:
        for lists_name in All_Units:
            for lists_value in lists_name:
                for unit in lists_value:
                    unit.y_lot += y_scroll_period - player.y_lot
        player.y_lot = y_scroll_period
    if player.y_lot > screen_height - player.height - y_scroll_period:
        for lists_name in All_Units:
            for lists_value in lists_name:
                for unit in lists_value:
                    unit.y_lot -= player.y_lot - (screen_height - player.height - y_scroll_period)
        player.y_lot = screen_height - player.height - y_scroll_period



class Unit:
    def __init__(self,image, x_lot, y_lot):
        self.image = pygame.image.load(image)
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.x_lot = x_lot
        self.y_lot = y_lot
        self.original_x = x_lot
        self.original_y = y_lot

    def bump(self,bump_unit):
        self.rect = self.image.get_rect()
        self.rect.left = self.x_lot
        self.rect.top = self.y_lot
        bump_unit_rect = bump_unit.image.get_rect()
        bump_unit_rect.left = bump_unit.x_lot 
        bump_unit_rect.top = bump_unit.y_lot - 1

        if self.rect.colliderect(bump_unit_rect):
            return True
        
    def cant_pass(self,bump_unit):
        global able_jump
        global jump_power
        self.rect = self.image.get_rect()
        self.rect.left = self.x_lot
        self.rect.top = self.y_lot
        bump_unit_rect = bump_unit.image.get_rect()
        bump_unit_rect.left = bump_unit.x_lot
        bump_unit_rect.top = bump_unit.y_lot - 1
        bump_unit_rect.right = bump_unit_rect.left + bump_unit.width
        bump_unit_rect.bottom = bump_unit.y_lot + bump_unit.height
        is_right = bump_unit_rect.right - player.x_lot
        is_left = player.x_lot - (bump_unit_rect.left - player.width)
        is_bottom = bump_unit_rect.bottom - player.y_lot
        is_top = player.y_lot - (bump_unit_rect.top - player.height)

        right_or_left = 1
        the_x_lot = 1
        top_or_bottom = 1
        the_y_lot = 1
        
        if self.bump(bump_unit):

            if is_left < is_right:
                right_or_left = is_left
                the_x_lot = (bump_unit_rect.left - player.width)
            elif is_left > is_right:
                right_or_left = is_right
                the_x_lot = bump_unit_rect.right
            else:
                right_or_left = 100

            if is_top < is_bottom:
                top_or_bottom = is_top
                able_jump = True
                the_y_lot = (bump_unit_rect.top - player.height)
            elif is_top > is_bottom:
                top_or_bottom = is_bottom
                able_jump = False
                the_y_lot = bump_unit_rect.bottom
            else:
                top_or_bottom = 100

            if right_or_left < top_or_bottom:
                player.x_lot = the_x_lot
                able_jump = False
                if top_or_bottom > 5:
                    global xspeed
                    xspeed = 0

            
            elif right_or_left > top_or_bottom:
                player.y_lot = the_y_lot
                if right_or_left > 5 and able_jump == False and jump_power > 0:
                    jump_power = 0

        else:
            able_jump = False
            global gravity
            gravity = Gravity

        if able_jump == True:
            jump_power = 0
            gravity = 0


    def move(self,xto):
        global xspeed,temp
        if game_condition == "pause":
            temp = xspeed
            xspeed = 0
        if game_condition == "continue":
            if xto == 0:
                    xspeed = xspeed * slide1
            xspeed += xto * slide2
            if abs(xto * speed * dt) <= -xspeed* speed * dt and xto != 0 or xspeed* speed * dt >= abs(xto * speed * dt) and xto != 0:
                xspeed = xto
            if creep == True:
                self.x_lot += xspeed * speed * dt * 0.5
            else:
                self.x_lot += xspeed * speed * dt


            for block in Blocks:
                player.cant_pass(block)
            scroll_move()


def jump(block):
    global gravity
    gravity = Gravity
    block.top = block.y_lot
    player.bottom = player.y_lot + player.height
    if player.bump(block) == True:
        if block.top - 2 < player.bottom < block.top + 2:
            if Jump == True:
                global jump_power
                jump_power = jump_power_set
    

def dead():
    global game_over_count,death_count,game_condition
    if death_count == game_over_count:
        death_count += 1
    game_condition = "game_over"

def restart():
    global dt , running , Jump  , PlayerXto, jump_power , xspeed, jump_power_set,\
          able_jump,right_pressed, left_pressed, Blocks, Enemies, All_Units,Savepoints,gravity,creep,Goals, player_spawnpoint
    
    
    gravity = Gravity
    right_pressed = False
    left_pressed =  False
    creep = False
    Jump = False
    PlayerXto = 0
    xspeed = 0

    jump_power = 0
    able_jump = False
    Blocks = []
    Savepoints = []
    Enemies = []
    All_Units = []
    Goals = []

    for unit in map_reading.map_read(map_file):
        if unit [0] == "block":
            Blocks.append(Unit(block_image,unit[1],unit[2]))
        elif unit [0] == "enemy":
            Enemies.append(Unit(enemy_image,unit[1],unit[2]))
        elif unit [0] == "savepoint":
            Savepoints.append(Unit(savepoint_image,unit[1],unit[2]))
        elif unit [0] == "goal":
            Goals.append(Unit(goal_image,unit[1],unit[2]))
    All_Units.append((Blocks,Enemies,Savepoints,Goals))

    player.x_lot = player_spawnpoint[0]
    player.y_lot = player_spawnpoint[1]

def x_move(right_pressed, left_pressed):
    global PlayerXto
    if right_pressed == left_pressed:
        PlayerXto = 0
    elif right_pressed == True:
        PlayerXto = 1
    else:
        PlayerXto = -1


#################################################################################################   
# My_Intial_Value -> def game_setting

play_mode = 0
map_file = os.listdir(f"{script_dir}//maps")[0]
def game_setting(play_mode):
    global map_file,player_image,enemy_image,block_image,savepoint_image,pause_image,goal_image,player,Blocks,Enemies,Savepoints,Goals,x_scroll_period,y_scroll_period,player_spawnpoint,death_count,game_over_count,speed,Gravity,jump_power_set,slide1,slide2
    player_image = f"{script_dir}\images//player{play_mode}.png"
    enemy_image = f"{script_dir}\images\enemy.png"
    block_image = f"{script_dir}\images//block.png"
    savepoint_image = f"{script_dir}\images//savepoint.png"
    pause_image = f"{script_dir}\images//pause.png"
    goal_image = f"{script_dir}\images//goal.png"
    if play_mode ==  3:
        player_image = f"{script_dir}\images//block.png"
        enemy_image = f"{script_dir}\images//block.png"
        block_image = f"{script_dir}\images//block.png"
        savepoint_image = f"{script_dir}\images//block.png"
        pause_image = f"{script_dir}\images//block.png"
        goal_image = f"{script_dir}\images//block.png"
    player = Unit(player_image, 0,0)
    Blocks = []
    Enemies = []
    Savepoints = []
    Goals = []
    x_scroll_period = 600
    y_scroll_period = 200
    player_spawnpoint = (0,0)
    game_over_count = 0
    speed = 0.5
    Gravity = 2.3
    jump_power_set = 90
    game_over_count = death_count
    
    slide1 =0.8
    slide2 =0.2
    if play_mode == 5:
        slide1 = 0.97
        slide2 = 0.03
        Gravity = 1.2
        speed = 0.6
        jump_power_set = 65
    if play_mode == 4:
        jump_power_set = 160
        Gravity =3
        speed = 3
        slide1 = 0.8
        slide2 = 0.03

        


game_setting(play_mode)


# My_Intial_Value 
################################################################################################

restart()
running = True
game_condition = "play_mode"
stage_point = 1000
pause_continue_time = 0


def main():
    global dt, running, PlayerXto, Jump , jump_power, right_pressed, left_pressed,click, game_condition,creep,xspeed,temp1
    
    if pygame.time.get_ticks() - pause_continue_time >= 1:
        if temp1 == temp2:
            xspeed = temp 
            temp1 += 1

    dt = clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                Jump = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                creep = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right_pressed = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left_pressed = True
            if event.key == pygame.K_ESCAPE:
                if PlayerXto == 0:
                    game_condition = "pause"


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                Jump = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                creep = False
            if event.key == pygame.K_RIGHT and right_pressed == True\
                or event.key == pygame.K_d and right_pressed == True:
                right_pressed = False
            if event.key == pygame.K_LEFT and left_pressed == True\
                or event.key == pygame.K_a and left_pressed == True:
                left_pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        x_move(right_pressed, left_pressed)

    pos = pygame.mouse.get_pos()
    global dont_draw_pause
    if PlayerXto == 0:
        dont_draw_pause = False
        if 10 < pos[0] < 60 and 10 < pos[1] < 60:
            pause_image = f"{script_dir}\images//pause2.png"
            if click == True:
                game_condition = "pause"
                pause_image = f"{script_dir}\images//pause.png"
        else:
            pause_image = f"{script_dir}\images//pause.png"
    else:
        dont_draw_pause = True

################################################################################################
# Unit Function
    for block in Blocks:
        jump(block)
    player.y_lot -= jump_power / 10 * dt /8
    jump_power -= gravity * dt /8
    
    player.move(PlayerXto)

    for enemy in Enemies:
        if player.bump(enemy) == True:
            dead()
    
    for goal in Goals:
        global clear_repeat
        if player.bump(goal) == True:
            game_condition = "clear"
            clear_repeat = pygame.time.get_ticks()
    
    for save in Savepoints:
        global player_spawnpoint
        if player.bump(save) == True:
            player_spawnpoint = [save.original_x,save.original_y]
            save.image = pygame.image.load(f"{script_dir}\images//savepoint2.png")
# Unit Function
################################################################################################
# Just_Fuction
    if Blocks[0].y_lot < Blocks[0].original_y -1000:
        dead()
# Just_Fuction        
################################################################################################
# Draw
    pygame.draw.rect(screen, BLACK, [0,0, screen_width,screen_height])
    for block in Blocks:
        player.cant_pass(block)
    for lists_name in All_Units:
        for lists_value in lists_name:
            for unit in lists_value:
                if play_mode == 2:
                    if 300 >= abs(player.y_lot-unit.y_lot)+abs(player.x_lot-unit.x_lot):
                        screen.blit(unit.image, (unit.x_lot, unit.y_lot))
                elif play_mode == 1:
                    if abs(unit.x_lot - player.x_lot) < 75:
                        screen.blit(unit.image, (unit.x_lot, unit.y_lot))
                    elif abs(unit.x_lot - player.x_lot) < 300:
                        screen.blit(unit.image, (unit.x_lot, unit.y_lot + abs(player.x_lot - unit.x_lot) * 0.3-20))
                    else:
                        screen.blit(unit.image, (unit.x_lot, unit.y_lot + abs(player.x_lot - unit.x_lot) * 0.8-170))
                else:
                    screen.blit(unit.image, (unit.x_lot, unit.y_lot))
    screen.blit(player.image, (player.x_lot, player.y_lot))

    if dont_draw_pause == False:
        screen.blit(pygame.image.load(pause_image),(10,10))
    text_print.text_printing(f"Death Count : {death_count}",870,20,WHITE)
    pygame.display.flip()
# Draw
################################################################################################
def Game_Over():
    global running , game_over_repeat ,dt, game_over_count, game_condition, right_pressed, left_pressed,creep,Jump
    right_pressed = False
    left_pressed =  False
    creep = False
    Jump = False
    if death_count > game_over_count:
        restart()
        game_over_repeat = pygame.time.get_ticks()
        game_over_count = death_count
    time =  pygame.time.get_ticks() - game_over_repeat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN) and time > 1333:
            restart()
            game_condition = "continue"
            dt = 0
    pygame.draw.rect(screen, BLACK, [0,0, screen_width,screen_height])
    screen.blit(pygame.image.load(f"{script_dir}//images//gameover.png"),(0,0))
    
    the_score = stage_point - death_count * 100
    if the_score < 0:
        the_score = 0

    if time >= 333:
        text_print.text_printing(f"{stage_point}P",380,158,WHITE)
    if time >= 666:
        text_print.text_printing(f"{death_count}",380,250,WHITE)
    if time >= 1000:
        if play_mode == 4:
            text_print.text_printing(f"You cant earn POINTS in this mode",380,350,RED)
        else:
            text_print.text_printing(f"{the_score}P",380,350,YELLOW)
    if 1333 <= time < 1833:
        text_print.text_printing("press Space Bar to restart",screen_width/2 - 300,screen_height/2 +200,WHITE)
    if 1833 <= time < 2333:
        text_print.text_printing("press Space Bar to restart",screen_width/2 - 300,screen_height/2 +200,GRAY)
    if time >= 2333:
        game_over_repeat = pygame.time.get_ticks() -1333
    pygame.display.flip()

def clear():
    global game_condition,running,clear_repeat, death_count, game_over_count
    the_score = stage_point - death_count * 100
    if the_score <0:
        the_score =0
    time = pygame.time.get_ticks() - clear_repeat 
    screen.blit(pygame.image.load(f"{script_dir}//images//clear.png"),(0,0))
    if time >= 333:
        text_print.text_printing(f"{stage_point}P",420,screen_height/2+5,WHITE)
    if time >= 666:
        text_print.text_printing(f"-{death_count * 100}P",420,screen_height/2 +67,WHITE)
    if time >= 1000:
        if play_mode == 4:
            text_print.text_printing(f"You cant earn POINTS in this mode",420,screen_height/2 +210,RED)
        else:
            text_print.text_printing(f"{the_score}P",420,screen_height/2 +210,YELLOW)
    if 1000 <= time < 1500:
        text_print.text_printing("Call the staff",screen_width/2+300,screen_height/2 +260,WHITE)
    if 1500 <= time < 2000:
        text_print.text_printing("Call the staff",screen_width/2+300,screen_height/2 +260,GRAY)
    if time >= 2000:
        clear_repeat = pygame.time.get_ticks() -1000
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_1):
                game_condition = "menu"
                death_count = 0
                game_over_count = 0


while running == True:
    if game_condition == "menu":
        game_condition = game_menu.start_menu()
    if game_condition == "game_restart":
        for unit in map_reading.map_read(map_file):
            if unit[0] == "player":
                global Initial_player_spawnpoint
                Initial_player_spawnpoint = [unit[1],unit[2]]
        player_spawnpoint = [Initial_player_spawnpoint[0],Initial_player_spawnpoint[1]]
        restart()
        game_condition = "continue"
    if game_condition == "game_over":
        right_pressed = False
        left_pressed =  False
        creep = False
        Jump = False
        Game_Over()
        xspeed = 0
    if game_condition == "quit":
        running = False
    if game_condition == "pause":
        right_pressed = False
        left_pressed =  False
        creep = False
        Jump = False
        game_condition = game_menu.pause()
        if game_condition == "continue":
            pause_continue_time  = pygame.time.get_ticks()
            temp2 += 1
    if game_condition == "continue":
        main()
    if game_condition == "stage":
        results = game_menu.stage(map_file)
        map_file = results[0]
        game_condition = results[1]
        if results[2] == 0:
            stage_point = 1000
        if results[2] == 1:
            stage_point = 2000
        if results[2] == 2:
            stage_point = 5000
    if game_condition == "clear":
        clear()
    if game_condition == "play_mode":
        game_condition = game_menu.play_mode()[0]
        play_mode = game_menu.play_mode()[1]
        game_setting(play_mode)
