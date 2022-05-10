''' Sam Gallagher 
    Space Invaders Projects
'''

## imports
import pygame
import sys
import random
## initliazing the pygame
pygame.init()

## creating the screen
screen = pygame.display.set_mode((800,600))

## Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('/home/sam/Projects/Space-Invaders/images/spaceship.png')
pygame.display.set_icon(icon)

## Player
playerImg = pygame.image.load('/home/sam/Projects/Space-Invaders/images/arcade-game.png')
playerX = 370
playerY= 480

## class of player
class Player():
    def __init__(self, img, x, y):

        ## image
        self.img = img
        ## starting x value
        self.x = x
        ## starting y value
        self.y = y

        self.health = 100


    def show(self):
        ## shows the player on the screen
        screen.blit(self.img, (self.x, self.y))
    def move(self, distance):
        ## updates the position of the spaceship
        
        if self.x+distance< 736 and self.x + distance > 0:
            self.x+=distance

    #
    # def shoot():
    #     ## shoots at the enemy
    #     pass
    # 
    # @property
    # def health():
    #     return self.health
    #


## enemy infromation
# enemyIMG = pygame.image.load('/home/sam/Projects/Space-Invaders/images/spaceship.png')
# enemyX = random.randint(0, 736)
# enemyy = 100
#
# class of the enemy
class Enemy():
    def __init__(self):
        self.x = random.randint(0, 736) 
        self.y = 100
        self.img =pygame.image.load('/home/sam/Projects/Space-Invaders/images/ghost.png')
        self.health = 50
    def show(self):
        screen.blit(self.img, (self.x, self.y))

#     def move():
#         ## moves in a random pattern
#         pass
#     
#     def health():
#         pass
#         
enemies = [Enemy() for i in range(10)]
player = Player(playerImg, playerX, playerY)
running = True
change = 0
## Game Loop
while running:
    ## fills the screen with RGB values
    screen.fill((0,0,0))
    for event in pygame.event.get():
        ## exits the loop when user quits program
        if event.type == pygame.QUIT:
            running = False

        ## runs if a arrow key is pressed
        elif event.type == pygame.KEYDOWN:

        
            ## if right arrow is pressed move right
            if event.key == pygame.K_RIGHT:
                # player.update(player.x+5)
                change = .3
                #
            ## if left arrow is pressed moves left
            elif event.key == pygame.K_LEFT:         
                change = -.3

        ## if not key is pressed spaceship does not move
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                change = 0

    ## moves the players
    player.move(change)
    ## shows the player
    player.show()
    for enemy in enemies:
        enemy.show()
    ## updates the display
    pygame.display.update()











