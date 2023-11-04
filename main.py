import os
import pygame
import map_reading
import text_print

pygame.init()
pygame.font.init()

script_dir = os.path.dirname(__file__)

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("super_mario")

#################################################################################################        

player_image = f"{script_dir}\images\player.png"
enemy_image = f"{script_dir}\images\enemy.png"
block_image = f"{script_dir}\images//block.png"
savepoint_image = f"{script_dir}\images//savepoint.png"

clock = pygame.time.Clock()
myFont = pygame.font.SysFont(None, 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

Blocks = []
Enemies = []
Savepoints = []


#################################################################################################
def scroll_move():
    for lists_name in All_Units:
        for lists_value in lists_name:
            for unit in lists_value:
                unit.x_lot -= xspeed * speed * dt
class Unit:
    def __init__(self,image, x_lot, y_lot):
        self.image = pygame.image.load(image)
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.x_lot = x_lot
        self.y_lot = y_lot

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
        global xspeed
        if xto == 0:
            xspeed = xspeed * 0.90
        xspeed += xto * 0.3
        if abs(xto * speed * dt) <= -xspeed* speed * dt and xto != 0 or xspeed* speed * dt >= abs(xto * speed * dt) and xto != 0:
            xspeed = xto
            
        self.x_lot += xspeed * speed * dt

        if self.x_lot < 300:
            self.x_lot = 300
            scroll_move()
        if self.x_lot > screen_width - self.width - 300:
            self.x_lot = screen_width - self.width -300
            scroll_move()

        if self.y_lot > screen_height - self.height:
            self.y_lot = screen_height - self.height
    
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
    

def summon_block(x_lot, y_lot):
    Blocks.append(Unit(block_image,x_lot,y_lot))

def summon_enemy(x_lot, y_lot):
    Enemies.append(Unit(enemy_image,x_lot,y_lot))

def summon_savepoint(x_lot,y_lot):
    Savepoints.append(Unit(savepoint_image,x_lot,y_lot))

def dead():
    global Count_down, game_over,death_count
    Count_down= False
    death_count += 1
    game_over = True

def restart():
    global dt , running , Jump , Dash , PlayerXto, jump_power , \
        game_start_count , xspeed, jump_power_set, able_jump,\
        right_pressed, left_pressed, Blocks, Enemies, All_Units,Savepoints
    right_pressed = False
    left_pressed =  False
    PlayerXto = 0
    xspeed = 0
    player.x_lot = 325
    player.y_lot = 400
    Jump = False
    jump_power = 0
    able_jump = False
    Blocks = []
    Savepoints = []
    Enemies = []
    All_Units = []

    for unit in map_reading.map_read("jump_game_map.txt"):
        if unit[0] == "_":
            pass
        elif unit [0] == "block":
            summon_block(unit[1],unit[2])
        elif unit [0] == "enemy":
            summon_enemy(unit[1],unit[2])
        elif unit [0] == "savepoint":
            summon_savepoint(unit[1],unit[2])
    All_Units.append((Blocks,Enemies,Savepoints))

def x_move(right_pressed, left_pressed):
    global PlayerXto
    if right_pressed == left_pressed:
        PlayerXto = 0
    elif right_pressed == True:
        PlayerXto = 1
    else:
        PlayerXto = -1


#################################################################################################   



player = Unit(player_image,0,0)

death_count = 0
game_over_count = 0
game_start_count = -1

speed = 0.5
Gravity = 2
gravity = Gravity
jump_power_set = 80





#################################################################################################

restart()

################################################################################################
running = True
game_over = False


def main():
    global dt, running, PlayerXto, Jump , Dash, jump_power, right_pressed, left_pressed
    dt = clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                Jump = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                Dash = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right_pressed = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                Jump = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                Dash = False
            if event.key == pygame.K_RIGHT and right_pressed == True\
                or event.key == pygame.K_d and right_pressed == True:
                right_pressed = False
            if event.key == pygame.K_LEFT and left_pressed == True\
                or event.key == pygame.K_a and left_pressed == True:
                left_pressed = False
        x_move(right_pressed, left_pressed)


    for block in Blocks:
        jump(block)
    player.y_lot -= jump_power / 10
    jump_power -= gravity
    
    player.move(PlayerXto)

    for enemy in Enemies:
        if player.bump(enemy) == True:
            dead()
    if player.y_lot >= 750:
        dead()

    pygame.draw.rect(screen, BLACK, [0,0, screen_width,screen_height])
    for block in Blocks:
        player.cant_pass(block)
    for lists_name in All_Units:
        for lists_value in lists_name:
            for unit in lists_value:
                screen.blit(unit.image, (unit.x_lot, unit.y_lot))
    screen.blit(player.image, (player.x_lot, player.y_lot))


    pygame.display.flip()

def Game_Over():
    global running , game_over_repeat , game_over_count, game_over, Count_down
    if death_count > game_over_count:
        restart()
        game_over_repeat = pygame.time.get_ticks()
        game_over_count = death_count
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and Count_down == True:
            game_over = False
    pygame.draw.rect(screen, BLACK, [0,0, screen_width,screen_height])
    text_print.text_printing("         GAME OVER",130,330,WHITE)


    if pygame.time.get_ticks() - game_over_repeat <333 and Count_down == False:
        text_print.text_printing("3",388,430,GRAY)
        pygame.display.flip()
    elif pygame.time.get_ticks() - game_over_repeat <666 and Count_down == False:
        text_print.text_printing("2",388,430,GRAY)
        pygame.display.flip()
    elif pygame.time.get_ticks() - game_over_repeat <999 and Count_down == False:
        text_print.text_printing("1",388,430,GRAY)
        pygame.display.flip()
    else:
        if pygame.time.get_ticks() - game_over_repeat < 500:
            text_print.text_printing("press any key to restart",130,430,WHITE)
            pygame.display.flip()
        elif pygame.time.get_ticks() - game_over_repeat < 1000:
            text_print.text_printing("press any key to restart",130,430,GRAY)
            pygame.display.flip()
        else:
            game_over_repeat = pygame.time.get_ticks()
            Count_down = True

while running == True:
    if game_over == False:
        main()
    if game_over == True:
        Game_Over()