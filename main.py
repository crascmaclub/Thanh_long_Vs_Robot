import pygame
import random

pygame.init() 

#Biến số
player_grav = 0 #Trọng lực
game_active = True
ground_y = 550
start_time = 0
start_timeR = 0
lives = 3

#Set up display mode
width, height = 1380, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

cras_logo = pygame.image.load("graphics/logo.jpg")
icon = pygame.display.set_icon(cras_logo)
caption = pygame.display.set_caption("Mì thanh long đại chiến robot")

#Background load img
sky = pygame.transform.scale(pygame.image.load("graphics/sky.png"), (width, height)).convert()
ground1 = pygame.transform.scale(pygame.image.load("graphics/ground1.png"), (width, height)).convert_alpha()
ground2 = pygame.transform.scale(pygame.image.load("graphics/ground2.png"), (width, height)).convert_alpha()
ground3 = pygame.transform.scale(pygame.image.load("graphics/ground3.png"), (width, height)).convert_alpha()
ground4 = pygame.transform.scale(pygame.image.load("graphics/ground4.png"), (width, height)).convert_alpha()
fullhearts = pygame.transform.scale(pygame.image.load("graphics/3hearts.png"),(150, 50)).convert_alpha()
twohearts = pygame.transform.scale(pygame.image.load("graphics/2hearts.png"),(150, 50)).convert_alpha()
heart = pygame.transform.scale(pygame.image.load("graphics/1heart.png"),(150, 50)).convert_alpha()
noheart = pygame.transform.scale(pygame.image.load("graphics/0heart.png"),(150, 50)).convert_alpha()
heart_rect = fullhearts.get_rect(topleft = (20, 20))

#Sprite obstacles
robot = pygame.transform.scale(pygame.image.load("graphics/robot.png"), (75, 100)).convert_alpha()
comprobot = pygame.transform.scale(pygame.image.load("graphics/comprobot.png"), (140, 90)).convert_alpha()
drone = pygame.transform.scale(pygame.image.load("graphics/drone.png"), (150, 75)).convert_alpha()
drone_rect = drone.get_rect(bottomleft = (1000, 200))

obs_rect_list = []

#Sprite mì thanh long
dragon = pygame.transform.scale(pygame.image.load("graphics/dragon.png"), (100, 200)).convert_alpha()
dragon_rect = dragon.get_rect(bottomleft = (100, ground_y))

#Font mặc định
default_font = pygame.font.Font("graphics/Pixeltype.ttf", 50)

#Bộ đếm tgian cho obs
obs_timer = pygame.USEREVENT +1
pygame.time.set_timer(obs_timer, 2000)

#Di chuyển của obs
def obs_movement(obs_list):
    if obs_list:
        for obs_rect in obs_list:
            obs_rect.x -= obs_speed
            if obs_rect.width == robot.get_width():
                screen.blit(robot, obs_rect)
            elif obs_rect.width == comprobot.get_width():
                screen.blit(comprobot, obs_rect)
            elif obs_rect.width == drone.get_width():
                screen.blit(drone, obs_rect)

        obs_list = [obs for obs in obs_list if obs.x > -200] #Xóa rect khi ra khỏi màn hình
        
        return obs_list
    else: 
        return []
#Va chạm
def collision(player, obs):
    if obs:
        for obs_rect in obs:
            if player.colliderect(obs_rect):
                return False
    return True
#Điểm
def score_display():
    global score
    score = pygame.time.get_ticks()/100 - start_time 
    score_surf = default_font.render(("Score: " + str(int(score))), False, "Red")
    score_rect = score_surf.get_rect(topright = (1365, 10))
    screen.blit(score_surf, score_rect)
#Mạng 
def live():
    if lives == 3:
        screen.blit(fullhearts, heart_rect)
    elif lives == 2:
        screen.blit(twohearts, heart_rect)
    elif lives == 1:
        screen.blit(heart, heart_rect)
    else:
        screen.blit(noheart, heart_rect)


#Main
while True:

    for event in pygame.event.get(): #Event ingame

        #Bấm nút quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Tgian cho obs spawn
        if event.type == obs_timer and game_active:
            if random.randint(0, 2) == 0:
                obs_rect_list.append(robot.get_rect(bottomleft = (random.randint(1380, 2000), 540)))
            elif random.randint(0, 2) == 1:
                obs_rect_list.append(comprobot.get_rect(bottomleft = (random.randint(1380, 2000), 540)))
            elif random.randint(0, 2) == 2:
                obs_rect_list.append(drone.get_rect(bottomleft = (random.randint(1380, 2000), 400)))
        
        #Bấm nút
        if event.type == pygame.KEYDOWN:
            #Bấm nút nhảy
            if event.key == pygame.K_SPACE and dragon_rect.bottom >= ground_y and game_active:
                player_grav = -22
            if event.key == pygame.K_UP and dragon_rect.bottom >= ground_y and game_active:
                player_grav = -22

            #Xoay ngang (trôn)
            if event.key == pygame.K_DOWN and dragon_rect.w == 100 and game_active:
                dragon = pygame.transform.rotate(dragon, -90)
                dragon_rect = dragon.get_rect(bottomleft = (100, dragon_rect.y+200))
                 
            #Bấm nút reset game
            if event.key == pygame.K_SPACE and game_active == False:
                dragon = pygame.transform.scale(pygame.image.load("graphics/dragon.png"), (100, 200)).convert_alpha()
                dragon_rect = dragon.get_rect(bottomleft = (100, ground_y))
                start_time = pygame.time.get_ticks()/100
                lives = 3
                game_active = True

        if event.type == pygame.KEYUP:
            #Trở về bth
            if event.key == pygame.K_DOWN and dragon_rect.w != 100 and game_active:
                dragon = pygame.transform.rotate(dragon, 90)
                dragon_rect = dragon.get_rect(bottomleft = (100, ground_y))
    
    
    if game_active: #Game đang chạy
        
        #Var
        obs_speed = 8 + float(int(pygame.time.get_ticks()/100 - start_time)/100)
        fall_sp = 1
        
        if obs_speed <= 8:
            fall_sp = 0.8      
        else:
            fall_sp = 1


        #Background
        counter = pygame.time.get_ticks() - start_timeR
        if int(counter/120)%4 == 0:
            ground = ground1
        if int(counter/120)%4 == 1:
            ground = ground2
        if int(counter/120)%4 == 2:
            ground = ground3
        if int(counter/120)%4 == 3:
            ground = ground4    

        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 0))

        score_display() #Score

        live() #Mạng

        #Main char
        player_grav += fall_sp
        dragon_rect.y += player_grav
        if dragon_rect.bottom > ground_y: 
            dragon_rect.bottom = ground_y

        screen.blit(dragon, dragon_rect)      

        #Obstacles
        obs_rect_list = obs_movement(obs_rect_list)

        #Va chạm
        if collision(dragon_rect, obs_rect_list) == False:
            lives -= 1
            if lives == 0:
                game_active = False
            else:
                obs_rect_list.clear()
                dragon = pygame.transform.scale(pygame.image.load("graphics/dragon.png"), (100, 200)).convert_alpha()
                dragon_rect = dragon.get_rect(bottomleft = (100, ground_y))

    else:#Thua
        screen.blit(default_font.render("Game Over", False, "Black"), (600, 300))
        obs_rect_list.clear()
        live()
        

    #Phần update screen liên tục
    pygame.display.update()
    clock.tick(60)
