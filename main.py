import pygame
import sys
from pygame.locals import *
import random as r
import time


clock = pygame.time.Clock()
pygame.init()
gameState = 0

playerName = 'Luminaar'
 
HEIGHT = 680
WIDTH = 1300

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fight It Out")

mianBg = pygame.transform.scale(pygame.image.load("images/main.png"),(WIDTH,HEIGHT))
startBg = pygame.transform.scale(pygame.image.load("images/start.png"),(WIDTH,HEIGHT))
selectBg = pygame.transform.scale(pygame.image.load("images/select.png"),(WIDTH,HEIGHT))
end1 = pygame.transform.scale(pygame.image.load("images/end1.png"),(WIDTH,HEIGHT))
end2 = pygame.transform.scale(pygame.image.load("images/end2.png"),(WIDTH,HEIGHT))
#players settings
playerHieght = 60
playerWidth = 60

playerX = -100
playerY = 230
enemyX = 520
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
    playerFrames = player.get_width()//288
    playerSheet = SpriteSheet(player)
    return player

def deathImage(name):
    return pygame.image.load(f"images/sprites/{name}/death.png").convert_alpha()

def attack(name,ty):
    return pygame.image.load(f"images/sprites/{name}/a{ty}.png").convert_alpha()

def hitImage(name):
    return pygame.image.load(f"images/sprites/{name}/hit.png").convert_alpha()

def spawnEnemy(name):
    global enemyFrames,enemySheet
    enemy = pygame.image.load(f"images/sprites/{name}/Idle.png").convert_alpha()
    enemyFrames = enemy.get_width()//288
    enemySheet = SpriteSheet(enemy)
    return enemy


playerAttackType = 0
enemyAttackType = 0

player = spawnPlayer('Seraphina')
enemy = spawnEnemy('Volcanus')

pFrameCheck = True
eFrameChcek = True

playerAttacking = False
enemyAttacking = False    

enemyGotHit =- False
playerGotHit = False

playerDied = False
enemyDied = False

edeathFrameCheck = False
pdeathFrameCheck = False

fonts = pygame.font.Font("font/font.otf",30)
hitcheck = True

class Player(pygame.sprite.Sprite): 
    def __init__(self,state='idle'):
        super().__init__()
        self.frame = 0
        self.state = state
        
        self.image = playerSheet.get_image(self.frame, 288, 128, 0, (0, 0, 0))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (playerX,playerY))

    def attack(self):
        global playerFrames,playerAttackSheet,pFrameCheck,playerAttackType,eFrameChcek,enemyAttacking,playerAttacking,playerHealth,enemyHealth,enemyGotHit  
        self.image = playerAttackSheet.get_image(int(self.frame % playerAttackframes), 288, 128, 3, (0, 0, 0))
        if pFrameCheck == True and self.frame != 0:
            self.frame = 0
            pFrameCheck = False
        if self.frame >= playerAttackframes:
                if playerAttackType == 1:
                    a = -(r.randint(5,30))
                    if enemyHealth + a < 0:
                        enemyHealth = 0
                    else:
                        enemyHealth += a
                    enemyGotHit = True


                elif playerAttackType == 2:
                    a = -(r.randint(10,20))
                    if enemyHealth + a < 0:
                        enemyHealth = 0
                    else:
                        enemyHealth += a
                    enemyGotHit = True

                elif playerAttackType == 3:
                    playerHealth += r.randint(5,15)
                    enemyAttacking = True
                

                pFrameCheck = True
                playerAttacking = False
                playerAttackType = 0
                self.state = 'idle'
                self.frame = 0

        self.frame += 0.1

    def idle(self):
        global playerAttacking,playerGotHit,playerDied,enemyGotHit
        self.image = playerSheet.get_image(int(self.frame % playerFrames), 288, 128, 3, (0, 0, 0))
        self.frame += 0.1
        if playerAttacking:
            self.state = 'attack'
        if playerGotHit:
            self.state = 'hit'
        if playerDied:
            self.state = 'death'

    def hit(self):
        global pHitFrames,pHitSheet,enemyAttacking,playerGotHit
        if self.frame != 0 and playerGotHit == True:
            self.frame = 0
            playerGotHit = False
        self.image = pHitSheet.get_image(int(self.frame%pHitFrames),288,128,3,(0,0,0))
        self.frame += 0.1
        if self.frame > pHitFrames:
            enemyAttacking = False
            self.frame = 0
            self.state = 'idle'

    def death(self):
        global pDeathSheet,pDeathFrames,gameState,playerDied,pdeathFrameCheck,playerHealth,enemyHealth
        self.image = pDeathSheet.get_image(int(self.frame % pDeathFrames), 288, 128, 3, (0, 0, 0))
        if self.frame != 0 and pdeathFrameCheck == False:
            self.frame = 0
            pdeathFrameCheck = True
        self.frame += 0.1
        if self.frame > eDeathFrames:
            self.frame = 0
            self.state = 'idle'
            pdeathFrameCheck = False
            playerDied = False
            gameState = 4



    def update(self):
        if self.state == 'hit':
            self.hit()
        elif self.state == 'idle':
            self.idle()
        elif self.state == 'attack':
            self.attack()
        elif self.state == 'death':
            self.death()



class Enemy(pygame.sprite.Sprite): 
    def __init__(self,state='idle'):
        super().__init__()
        self.frame = 0
        self.state = state
        
        self.image = enemySheet.get_image(self.frame, 288, 128, 0, (0, 0, 0))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (enemyX,enemyY))

    def idle(self):
        global enemyAttacking,enemyGotHit,enemyDied
        self.image = pygame.transform.flip(enemySheet.get_image(int(self.frame % enemyFrames),288, 128, 3, (0,0,0)), True, False)
        self.frame += 0.1
        if enemyAttacking:
            self.state = 'attack'
        if enemyGotHit:
            self.state = 'hit'
        if enemyDied:
            self.state = 'death'

    def hit(self):
        global eHitFrames,eHitSheet,enemyAttacking,hitcheck,playerAttacking,enemyGotHit
        if self.frame != 0 and hitcheck == True:
            self.frame = 0
            hitcheck = False
        self.image = pygame.transform.flip(eHitSheet.get_image(int(self.frame%eHitFrames),288,128,3,(0,0,0)),True,False)
        self.frame += 0.1
        if self.frame > eHitFrames:
            enemyGotHit = False
            enemyAttacking = True
            self.frame = 0
            self.state = 'idle'



    def death(self):
        global eDeathSheet,eDeathFrames,gameState,enemyDied,edeathFrameCheck,playerHealth,enemyHealth
        self.image = eDeathSheet.get_image(int(self.frame % eDeathFrames), 288, 128, 3, (0, 0, 0))
        if self.frame != 0 and edeathFrameCheck == False:
            self.frame = 0
            edeathFrameCheck = True
        self.frame += 0.1
        if self.frame > eDeathFrames:
            self.frame = 0
            edeathFrameCheck = False
            enemyDied = False
            self.state = 'idle'
            gameState = 4




    

    def attack(self):
        global enemyAttackSheet,eFrameChcek,playerAttacking,enemyAttacking,playerHealth,enemyAttackType,enemyHealth,playerGotHit
        self.image = pygame.transform.flip(enemyAttackSheet.get_image(int(self.frame % enemyAttackframes), 288, 128, 3, (0, 0, 0)),True,False)
        if eFrameChcek == True and self.frame != 0:
            self.frame = 0
            eFrameChcek = False
        if self.frame >= enemyAttackframes:
                if enemyAttackType == 1:
                    a = -r.randint(15,25)
                    if playerHealth + a < 0:
                        playerHealth = 0
                    else:
                        playerHealth += a
                    playerGotHit = True
                elif enemyAttackType == 2:
                    a = -r.randint(5,35)
                    if playerHealth + a < 0:
                        playerHealth = 0
                    else:
                        playerHealth += a
                    playerGotHit = True
                elif enemyAttackType == 3:
                    enemyHealth += r.randint(10,20)
                
                enemyAttacking = False
                eFrameChcek = True
                self.state = 'idle'
                self.frame = 0
        self.frame += 0.1

    def update(self):   
        if self.state == 'hit':
            self.hit()
        elif self.state == 'idle':
            self.idle()
        elif self.state == 'attack' and enemyHealth > 0:
            self.attack()
        elif self.state == 'death':
            self.death()



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
    pimg = pygame.transform.scale(pygame.image.load(f"images/sprites/{playerName}/dp.png"),(80,80 ))
    eimg = pygame.transform.scale(pygame.image.load(f"images/sprites/{enemyName}/dp.png"),(80,80 ))
    text = fonts.render(f'{playerName}', True,"black")
    health = fonts.render(f'Health: {playerHealth}', True,"black")
    screen.blit(health, (340, 80))
    screen.blit(text, (340, 115))
    screen.blit(pimg,(250,70))
    text = fonts.render(f'{enemyName}', True,"black")
    health = fonts.render(f'Health: {enemyHealth}', True,"black")
    screen.blit(health, (800, 80))
    screen.blit(text, (800, 115))
    screen.blit(eimg,(990,70))


enemyName = 'Volcanus'
enum = 6
pnum = 3
chrdict = {1:'Ferrus',2:'Luminaar',3:'Seraphina',4:'Verdant',5:'Stonefist',6:'Volcanus',7:'Whispyr'}

while  True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYDOWN:
            if gameState == 3 and playerAttackType == 0 and enemyAttacking == False:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    playerAttackType = 1

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    playerAttackType = 2

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    playerAttackType = 3

                if playerAttackType != 0 and enemyAttacking == False and enemyGotHit == False: 
                    enemyAttackType = r.randint(1,3)
                    playerAttacking = True

                    eAttack = attack(enemyName,enemyAttackType)
                    pAttack = attack(playerName,playerAttackType)
                    playerAttackSheet = SpriteSheet(pAttack)
                    enemyAttackSheet = SpriteSheet(eAttack)
                    playerAttackframes = pAttack.get_width()//288
                    enemyAttackframes = eAttack.get_width()//288

                    pHit = hitImage(playerName)
                    eHit = hitImage(enemyName)
                    pHitSheet = SpriteSheet(pHit)
                    eHitSheet = SpriteSheet(eHit)
                    pHitFrames = pHit.get_width()//288
                    eHitFrames = eHit.get_width()//288

                    pDeath = deathImage(playerName)
                    eDeath = deathImage(enemyName)
                    pDeathSheet = SpriteSheet(pDeath)
                    eDeathSheet = SpriteSheet(eDeath)
                    pDeathFrames = pDeath.get_width()//288
                    eDeathFrames = eDeath.get_width()//288


            if gameState == 1:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pnum = (pnum%7)+1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if pnum == 1:
                        pnum = 5
                    else:
                        pnum -= 1
                playerName = chrdict[pnum]    
                player = spawnPlayer(playerName)

                if event.key == K_RETURN:
                    gameState = 2
                    lastKeytime = pygame.time.get_ticks()

            if gameState == 2:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    enum = (enum%7)+1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if enum == 1:
                        enum = 5
                    else:
                        enum -= 1

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    currentKeyTime = pygame.time.get_ticks()
                    if currentKeyTime - lastKeytime > 300:
                        gameState += 1

                enemyName = chrdict[enum]
                spawnEnemy(enemyName)

            if event.key == pygame.K_RETURN and gameState == 0:
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

    #main game
    if gameState == 3:
        window()
        players.update()
        enemy.update()
        displayHealth()  
        if enemyHealth <= 0 or playerHealth <= 0:
            playerGotHit,enemyGotHit = False,False
            enemyAttacking = False
            playerAttacking = False
            if playerHealth <= 0:
                playerDied = True
                endscreen = 1
            if enemyHealth <= 0:
                enemyDied = True
                endscreen = 2

    #gameover screen
    if gameState == 4:
        enemyDied,playerDied = False,False  
        if endscreen==1:
            screen.blit(end2,(0,0))
        elif endscreen == 2:
            screen.blit(end1,(0,0))
        enemyHealth = 1
        playerHealth = 1
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            gameState = 0


    pygame.display.update()
    clock.tick(300)
