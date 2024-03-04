import pygame
import sys
from pygame.locals import *
import random as r
import time


clock = pygame.time.Clock()
pygame.init()
gameState = 0


HEIGHT = 700
WIDTH = 1300

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fight It Out")

bg = pygame.transform.scale(pygame.image.load("images/City2.png"),(1300,700))

sbg = pygame.transform.scale(pygame.image.load("images/a.png"),(1300,700))


#players settings
playerHieght = 60
playerWidth = 60

playerX = 0
playerY = 230
enemyX = 950
enemyY = 230




class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height),pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image




pname = 'boy'
player = pygame.image.load(f"images/sprites/{pname}/Idle.png").convert_alpha()
ifm = player.get_width()//player.get_height()
pSheet = SpriteSheet(player)


ename = 'girl'
enemy = pygame.image.load(f"images/sprites/{ename}/Idle.png").convert_alpha()
eSheet = SpriteSheet(enemy)
efm = enemy.get_width()//enemy.get_height()
'''
eAttack = pygame.image.load("images/sprites/boy/a1.png").convert_alpha()
eAttackSheet = SpriteSheet(eAttack)
'''


myAttack = 0
flag = True



class Player(pygame.sprite.Sprite): 
    def __init__(self,state='idle'):
        super().__init__()
        self.frame = 0
        self.state = state
        
        self.image = pSheet.get_image(self.frame, 128, 128, 0, (0, 0, 0))
        self.rect = self.image.get_rect(center = (playerX,playerY))

    def animate(self):
        global myAttack,flag,ifm
 
        if myAttack != 0:
            if self.frame != 0 and flag == True:
                self.frame = 0
                flag = False
            self.state = 'attack'

        self.frame += 0.1
        if self.state == 'idle':
            self.image = pSheet.get_image(int(self.frame % ifm), 128, 128, 3, (0, 0, 0))

        if self.state == 'attack':
            self.image = pAttackSheet.get_image(int(self.frame % afm), 128, 128, 3, (0, 0, 0))
            if self.frame >= afm:
                self.state = 'idle'
                self.frame = 0
                myAttack = 0
                flag = True

    def update(self):
        self.animate()

class Enemy(pygame.sprite.Sprite): 
    def __init__(self,state='idle'):
        super().__init__()
        self.frame = 0
        self.state = state
        
        self.image = eSheet.get_image(self.frame, 128, 128, 0, (0, 0, 0))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (enemyX,enemyY))

    def animate(self):
        self.frame += 0.1
        if self.state == 'idle':
            self.image = pygame.transform.flip(eSheet.get_image(int(self.frame % efm), 128, 128, 3, (0, 0, 0)), True, False)

        if self.state == 'attack':
            self.image = pAttackSheet.get_image(int(self.frame % afm), 128, 128, 3, (0, 0, 0))
            if self.frame >= afm:
                self.state = 'idle'
                self.frame = 0
                myAttack = 0
                flag = True

    def update(self):
        self.animate()





#character defination
players = pygame.sprite.GroupSingle()
players.add(Player())


enemy = pygame.sprite.GroupSingle()
enemy.add(Enemy())

def start():
    screen.blit(sbg,(0,0))
    pygame.display.update()

def window():
    screen.blit(bg,(0,0))
    players.draw(screen)
    enemy.draw(screen)

def playerAttack(name,att):
    global myAttack
    myAttack = att
    return pygame.image.load(f"images/sprites/{name}/a{att}.png").convert_alpha()


while  True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if gameState == 1 and myAttack == 0:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    pAttack = playerAttack(pname,1)

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    pAttack = playerAttack(pname,2)

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pAttack = playerAttack(pname,3)

                if myAttack != 0:
                    pAttackSheet = SpriteSheet(pAttack)
                    afm = pAttack.get_width()//pAttack.get_height()

            if event.type == 768:
                gameState = 1
          
    if gameState == 0:
        start()

    if gameState == 1:
        window()
        players.update()
        enemy.update()
        pygame.display.update()
    clock.tick(60)