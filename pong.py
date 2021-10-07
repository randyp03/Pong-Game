import pygame, sys, random

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('My Pong Game')

WINDOW_SIZE = (1280, 720)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

# player
player = pygame.Rect(10,(WINDOW_SIZE[1]/2 - 100),25,100)

# computer
computer = pygame.Rect((WINDOW_SIZE[0] - 35),(WINDOW_SIZE[1]/2 - 100),25,100)

# ball
ball = pygame.Rect((WINDOW_SIZE[0]/2 - 25),(WINDOW_SIZE[1]/2 - 25),25,25)
ball_speed_x = 9
ball_speed_y = 9

# score variables
player_score = 0
computer_score = 0
game_font = pygame.font.Font("freesansbold.ttf",28)

def ball_movement(player_score,computer_score): 
    # ball will bounce off walls and off players
    global ball_speed_x, ball_speed_y
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= WINDOW_SIZE[1]:
        ball_speed_y *= -1

    if ball.left <= 0:
        computer_score += 1
        ball_start()

    if ball.right >= WINDOW_SIZE[0]:
        player_score += 1
        ball_start()

    if ball.colliderect(player) or ball.colliderect(computer):
        ball_speed_x *= -1

    return player_score,computer_score

def player_movement(player,speed): 
    # player will not be able to move out of the window
    player.y += speed[1]
    if player.bottom >= WINDOW_SIZE[1]:
        player.bottom = WINDOW_SIZE[1]
    if player.top <= 0:
        player.top = 0

def computer_movement(ball,computer,speed): 
    # computer AI to follow ball and not fall out of view in window
    if ball.y > computer.bottom:
        computer.y += speed[1]
    if ball.y < computer.top:
        computer.y -=speed[1]
    if computer.bottom >= WINDOW_SIZE[1]:
        computer.bottom = WINDOW_SIZE[1]
    if computer.top <= 0:
        computer.top = 0

def ball_start():
    global ball_speed_x, ball_speed_y

    ball.center = ((WINDOW_SIZE[0]/2),(WINDOW_SIZE[1]/2))
    ball_speed_x *= random.choice((1,-1))
    ball_speed_y *= random.choice((1,-1))
    
up = False
down = False
right = False
left = False

# game loop
while True:

    player_speed = [0,0]
    if up == True:
        player_speed[1] -= 10
    if down == True:
        player_speed[1] += 10

    # event getter
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
        if event.type == KEYUP:
            if event.key == K_UP:
                up = False
            if event.key == K_DOWN:
                down = False
                
    # movement
    player_movement(player,player_speed)

    computer_speed = [9,9]
    computer_movement(ball,computer,computer_speed)
    
    # return score based on ball collision
    player_score, computer_score = ball_movement(player_score,computer_score)     

    # visuals
    screen.fill('grey12')
    pygame.draw.aaline(screen,'white',(WINDOW_SIZE[0]/2,0),(WINDOW_SIZE[0]/2,WINDOW_SIZE[1]))
    pygame.draw.rect(screen,'white',player)
    pygame.draw.rect(screen,'white',computer)
    pygame.draw.ellipse(screen,'white',ball)

    # game score keeper
    player_text = game_font.render(f"{player_score}",False,"white")
    screen.blit(player_text,(600,450))
    computer_text = game_font.render(f'{computer_score}',False,'white')
    screen.blit(computer_text,(660,450))

      
    pygame.display.update()
    clock.tick(60)
