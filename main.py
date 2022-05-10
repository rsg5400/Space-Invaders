''' Sam Gallagher 
    Space Invaders Projects
'''

## imports
import pygame
import sys
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

    def show(self):
        ## shows the player on the screen
        screen.blit(self.img, (self.x, self.y))
    def update(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


## class of the enemy
class Enemy():
    def __init__(self):
        pass


player = Player(playerImg, playerX, playerY)
running = True
## Game Loop
while running:
    ## fills the screen with RGB values
    screen.fill((0,0,0))
    for event in pygame.event.get():
        ## exits the loop when user quits program
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

        
            if event.key == pygame.K_RIGHT:
                player.update(player.x+5,player.y)

            elif event.key == pygame.K_LEFT:         
                player.update(player.x-5,player.y)

        # elif event.type == pygame.KEYUP:
        #
        #         player.update(player.x-5,player.y)


    player.show()

    ## updates the display
    pygame.display.update()











