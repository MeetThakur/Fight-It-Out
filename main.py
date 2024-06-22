import pygame
import sys
from pygame.locals import *
import random as r
import time


clock = pygame.time.Clock()
pygame.init()
gameState = 0

playerName = 'Zephyr'

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

playerHealth = 100
enemyHealth = 100

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height),pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image

def spawnPlayer(name):
    global playerFrames,playerSheet
    player = pygame.image.load(f"images/sprites/{name}/Idle.png").convert_alpha()
    playerFrames = player.get_width()//player.get_height()
    playerSheet = SpriteSheet(player)
    return player



def playerAttack(name,ty):
    global playerAttackType
    playerAttackType = ty
    return pygame.image.load(f"images/sprites/{name}/a{ty}.png").convert_alpha()


def spawnEnemy(name):
    global enemyFrames,enemySheet
    enemy = pygame.image.load(f"images/sprites/{name}/Idle.png").convert_alpha()
    enemyFrames = enemy.get_width()//enemy.get_height()
    enemySheet = SpriteSheet(enemy)
    return enemy


def enemyAttack(name,ty):
    global enemyAttackType
    enemyAttackType = ty
    return pygame.image.load(f"images/sprites/{name}/a{ty}.png").convert_alpha()



player = spawnPlayer('Aetheria')
enemy = spawnEnemy('Nekros')


playerAttackType = 0
enemyAttackType = 0
isPlayerAttacking = False
isEnemyAttaking = False



class Player(pygame.sprite.Sprite): 
    def __init__(self,state='idle'):
        super().__init__()
        self.frame = 0
        self.state = state
        
        self.image = playerSheet.get_image(self.frame, 128, 128, 0, (0, 0, 0))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (playerX,playerY))

    def attack(self):
        global playerFrames,playerAttackSheet,isPlayerAttacking,playerAttackType
        self.image = playerAttackSheet.get_image(int(self.frame % attackFrames), 128, 128, 3, (0, 0, 0))
        print(self.frame)
        if isPlayerAttacking == True and self.frame != 0:
            self.frame = 0
            isPlayerAttacking = False
        if self.frame >= attackFrames:
                self.state = 'idle'
                self.frame = 0
                playerAttackType = 0
        self.frame += 0.1

    def idle(self):
        global isPlayerAttacking
        self.image = playerSheet.get_image(int(self.frame % playerFrames), 128, 128, 3, (0, 0, 0))
        self.frame += 0.1
        if isPlayerAttacking:
            self.state = 'attack'


    def update(self):
        if self.state == 'idle':
            self.idle()
        elif self.state == 'attack':
            self.attack()


class Enemy(pygame.sprite.Sprite): 
    def __init__(self,state='idle'):
        super().__init__()
        self.frame = 0
        self.state = state
        
        self.image = enemySheet.get_image(self.frame, 128, 128, 0, (0, 0, 0))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (enemyX,enemyY))

    def idle(self):
        global isEnemyAttaking
        self.image = pygame.transform.flip(enemySheet.get_image(int(self.frame % enemyFrames),128, 128, 3, (0,0,0)), True, False)
        self.frame += 0.1
        if isEnemyAttaking:
            self.state = 'attack'

    def attack():
        global eshee,isPlayerAttacking,playerAttackType
        self.image = eshee.get_image(int(self.frame % attackFrames), 128, 128, 3, (0, 0, 0))
        print(self.frame)
        if isPlayerAttacking == True and self.frame != 0:
            self.frame = 0
            isPlayerAttacking = False
        if self.frame >= attackFrames:
                self.state = 'idle'
                self.frame = 0
                playerAttackType = 0
        self.frame += 0.1

    def update(self):
        self.idle()




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

def displayHealth():
    font = pygame.font.Font(None, 50)
    text = font.render(f'Player Health: {playerHealth}', True,"white", (0, 0, 0))
    screen.blit(text, (10, 10))
    text = font.render(f'Enemy Health: {enemyHealth}', True,"white", (0, 0, 0))
    screen.blit(text, (970, 10))


ename = 'Nekros'
chrnum = 3
chrdict = {1:'Zephyr',2:'Elysia',3:'Aetheria',4:'Nekros',5:'Synthos'}

while  True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



        if event.type == pygame.KEYDOWN:
            if gameState == 3 and playerAttackType == 0:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    pAttack = playerAttack(playerName,1)

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    pAttack = playerAttack(playerName,2)

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pAttack = playerAttack(playerName,3)

                if playerAttackType != 0: 
                    isPlayerAttacking = True
                    eAttcak = (enemyName,r)
                    playerAttackSheet = SpriteSheet(pAttack)
                    attackFrames = pAttack.get_width()//pAttack.get_height()


            if gameState == 1:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    chrnum = (chrnum%5)+1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if chrnum == 1:
                        chrnum = 5
                    else:
                        chrnum -= 1
                playerName = chrdict[chrnum]    
                player = spawnPlayer(playerName)

                if event.key == K_SPACE:
                    gameState = 2

            if gameState == 2:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    chrnum = (chrnum%5)+1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if chrnum == 1:
                        chrnum = 5
                    else:
                        chrnum -= 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == 13:
                        gameState = 3

                enemyName = chrdict[chrnum]
                spawnEnemy(enemyName)

            if event.key == 13 and gameState == 0:
                gameState = 1
          

    #homescreen
    if gameState == 0:
        start()

    #player selection
    if gameState == 1:
        select()
        players.draw(screen)
        players.update()

    #enemy selection
    if gameState == 2:
        select()
        players.draw(screen)
        players.update()
        enemy.draw(screen)
        enemy.update()

    if gameState == 3:
        window()
        players.update()
        enemy.update()
        displayHealth()

    pygame.display.update()
    clock.tick(60)
