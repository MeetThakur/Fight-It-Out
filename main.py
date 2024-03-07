import pygame
import sys
from pygame.locals import *
import random as r
import time


clock = pygame.time.Clock()
pygame.init()
gameState = 0

pname = 'Zephyr'

HEIGHT = 700
WIDTH = 1300

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fight It Out")


mianBg = pygame.transform.scale(pygame.image.load("images/main.png"),(1300,700))
startBg = pygame.transform.scale(pygame.image.load("images/start.png"),(1300,700))
selectBg = pygame.transform.scale(pygame.image.load("images/select.png"),(1300,700))



#players settings
playerHieght = 60
playerWidth = 60

playerX = 0
playerY = 230
enemyX = 900
enemyY = 230




class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height),pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image



def spawnPlayer(name):
    global ifm,pSheet
    player = pygame.image.load(f"images/sprites/{name}/Idle.png").convert_alpha()
    ifm = player.get_width()//player.get_height()
    pSheet = SpriteSheet(player)
    return player

def playerAttack(name,att):
    global myAttack
    myAttack = att
    return pygame.image.load(f"images/sprites/{name}/a{att}.png").convert_alpha()

player = spawnPlayer('Aetheria')




def spawnEnemy(name):
    global efm,eSheet
    enemy = pygame.image.load(f"images/sprites/{name}/Idle.png").convert_alpha()
    efm = enemy.get_width()//enemy.get_height()
    eSheet = SpriteSheet(enemy)
    return enemy

enemy = spawnEnemy('Aetheria')




'''
eAttack = pygame.image.load("images/sprites/Zephyr/a1.png").convert_alpha()
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
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (450,playerY))

            
    def animate(self):
        global myAttack,flag,ifm
        if gameState == 2:
            self.rect = self.image.get_rect(center = (200,420))
        if myAttack != 0:
            if self.frame != 0 and flag == True:
                self.frame = 0
                flag = False
            self.state = 'attack'

        self.frame += 0.1
        if pname == 'Elysia' and self.state == 'idle':
            if int(self.frame%ifm) == 1:
                self.frame = 2.1
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
    screen.blit(startBg,(0,0))

def select():
    screen.blit(selectBg,(0,0))

def window():
    screen.blit(mianBg,(0,0))
    players.draw(screen)
    enemy.draw(screen)

ename = 'Nekros'
chrnum = 1
chrdict = {1:'Zephyr',2:'Elysia',3:'Aetheria',4:'Nekros',5:'Synthos'}

while  True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if gameState == 2 and myAttack == 0:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    pAttack = playerAttack(pname,1)

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    pAttack = playerAttack(pname,2)

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pAttack = playerAttack(pname,3)

                if myAttack != 0: 
                    pAttackSheet = SpriteSheet(pAttack)
                    afm = pAttack.get_width()//pAttack.get_height()


            if gameState == 1:
                if event.key == pygame.K_RIGHT:
                    chrnum = (chrnum%5)+1
                elif event.key == pygame.K_LEFT:
                    if chrnum == 1:
                        chrnum = 5
                    else:
                        chrnum -= 1
                pname = chrdict[chrnum]
                player = spawnPlayer(pname)
                playerX = 0
                if event.key == 13:
                    gameState = 2



            if event.key == 13 and gameState == 0:
                gameState = 1
          



    if gameState == 0:
        start()
    if gameState == 1:
        select()
        players.draw(screen)
        players.update()

    if gameState == 2:
        window()
        players.update()
        enemy.update()


    pygame.display.update()
    clock.tick(60)
