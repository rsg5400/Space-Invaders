## Imports
import pygame
import os 
import time
import random

pygame.init()

width, height = 750, 750

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders: By Sam Gallagher")

## Images

icon = pygame.image.load('/home/sam/Projects/Space-Invaders/images/spaceship.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('/home/sam/Projects/Space-Invaders/images/arcade-game.png')

enemyImg = pygame.image.load('/home/sam/Projects/Space-Invaders/images/space-ship.png')

## class of a the main ship
class Ship():

    def __init__(self, xPosition, yPosition, health = 100, pixels = 64):
        ## X and Y position
        self.x = xPosition
        self.y = yPosition 
        self.pixels = pixels
        ## ship health
        self.health = health
        self.img = None 



    def draw(self):
        ## draws the ship
        screen.blit(self.img, (self.x, self.y))


    def shoot(self):
        pass
class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = playerImg

    

class Enemy(Ship):
    def __init__(self, pixels = 64):
        self.pixels = pixels
        self.x = random.randint(0, width-self.pixels)
        self.y = random.randint(0, 200)
        self.img = enemyImg
    def move(self,velo):
        self.y += velo


    
def main():
    run = True
    FPS=60
    velocity = 5
    enemy_velocity = 2
    clock = pygame.time.Clock()
    # enemy=Enemy()
    enemies = [Enemy() for i in range(6)]

    ship = Player(350,600)
    
    def screen_update():
        screen.fill((0,0,0))

        ship.draw()
        for enemy in enemies:

            enemy.draw()
        pygame.display.update()

    while run:
        clock.tick(FPS)
        screen_update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        ## moves the ship around

        if keys[pygame.K_a] and ship.x>=0:
            ship.x -= velocity
        elif keys[pygame.K_d] and ship.x <= width-ship.pixels:
            ship.x += velocity

        elif keys[pygame.K_w] and ship.y >= 0:
            ship.y -= velocity

        elif keys[pygame.K_s] and ship.y <=height-ship.pixels:
            ship.y += velocity
        ## moves the enemy
        for enemy in enemies:

            enemy.move(enemy_velocity)




        


main()
