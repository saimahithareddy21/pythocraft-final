import pygame
import random
from pygame import mixer
import math
import time
from tkinter import messagebox
no_of_chickens=20
no_of_enemies=3
pygame.init()
chick_positions = [(690, 50), (720, 100), (690, 150), (720, 200)]
screen = pygame.display.set_mode((800, 700))
# icon and caption
pygame.display.set_caption('poulterer')
icon = pygame.image.load('001-chicken.png')
pygame.display.set_icon(icon)
# bgm
bgm=mixer.music.load('mixkit-forest-near-countryside-farm-1221.wav')
mixer.music.play(-1)
# chick
chicks = [pygame.image.load('001-chickenimg.png')] * 4
chickX = 900
chickY = 100
# player
playerImg = pygame.image.load('001-man.png')
playerX = 370
playerY = 520
playerX_change = 0
# enemy
enemyImg =[]
enemyX =[]
enemyY =[]
enemyX_change = 0.5
enemyY_change = 0.5
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('001-fox.png'))
    enemyX.append( random.randint(30, 600))
    enemyY.append(random.randint(50,150))

# ballon throwing
ballonImg = pygame.image.load('001-water-balloons.png')
ballon_state = 'ready'
ballonX = playerX
ballonY = playerY - 16
ballonX_change = 0
ballonY_change = 1
ballon_state = 'ready'

# score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
def player(x, y):
    screen.blit(playerImg, (x, y))


def throw_balloons(x, y):
    global ballon_state
    ballon_state = 'fire'
    screen.blit(ballonImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))

def iscollision(x1,y1,x2,y2):
    distance=math.dist([x1,y1],[x2,y2])
    if distance<=120:
        return True
    else:
        return False
# game over display
game_over_text=pygame.font.Font('freesansbold.ttf',50)
def gameover_display():
    gameover=game_over_text.render('Game over',True,(255,0,0))
    screen.blit(gameover,(250,280))
def score_display():
    score=font.render('score:'+str(score_value),True,(0,0,0))
    screen.blit(score,(10,10))
running = True
while running:
    screen.fill((153, 255, 153))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                ballonX = playerX
                ballonsound = mixer.Sound('mixkit-cartoon-bubbles-popping-732.wav')
                ballonsound.play()
                throw_balloons(ballonX, ballonY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX >= 686:
        playerX = 686
    if playerX <= -20:
        playerX = -20
    i = 0
    for chick in chicks:
        # there are many chicks , here I have taken if you have only 4 chicks
        screen.blit(chick, (chick_positions[i]))
        i += 1
    if ballonY <= 0:
        ballon_state = 'ready'
        ballonY = playerY - 16
    if ballon_state == 'fire':
        ballonY -= ballonY_change
        throw_balloons(ballonX + 78, ballonY)
    if no_of_chickens==0:
        for i in range(no_of_enemies):
            enemyX[i] = 2000
            enemyY[i]=2000
            enemy(enemyX[i],enemyY[i],i)
        player(playerX, playerY)
        gameover_display()

        pygame.display.update()
        time.sleep(1)
        break
    for i in range(no_of_enemies):
        enemyX[i]+= enemyX_change
        enemy(enemyX[i], enemyY[i],i)
        if enemyX[i]>=630:
            enemyX[i] = 20
            enemyY[i] = random.randint(50,150)
            no_of_chickens-=1
        if iscollision(enemyX[i],enemyY[i],ballonX,ballonY):
            explosionsound = mixer.Sound('explosion.wav')
            explosionsound.play()
            ballon_state='ready'
            ballonY=playerY-16
            enemyX[i]=random.randint(10,500)
            enemyY[i]=random.randint(50,150)
            score_value+=1
    player(playerX, playerY)

    score_display()
    pygame.display.update()
messagebox.showinfo('total score',str(score_value))
