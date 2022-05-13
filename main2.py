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

## class for the lasers
class Laser():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('/home/sam/Projects/Space-Invaders/images/icons8-vertical-line-48.png')
        

    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        self.move(5)

    def move(self, velo):
        self.y -= velo

    def hit(self):
        pass



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
        self.lasers = []



    def draw(self):
        ## draws the ship
        screen.blit(self.img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw()

    def shoot(self, current, shot):

        if current-shot > 350:
            laser = Laser(self.x+self.pixels*.15, self.y - .8*self.pixels)

            self.lasers.append(laser)
            return True
        else:
            return False

        



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
        self.lasers = []
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

    player = Player(350,600)
    current_time = 0
    shoot_time = 0
    
    def screen_update():
        screen.fill((0,0,0))

        player.draw()


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

        if keys[pygame.K_a] and player.x>=0:
            player.x -= velocity
        elif keys[pygame.K_d] and player.x <= width-player.pixels:
            player.x += velocity

        elif keys[pygame.K_w] and player.y >= 0:
            player.y -= velocity

        elif keys[pygame.K_s] and player.y <=height-player.pixels:
            player.y += velocity

        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            if player.shoot(current_time, shoot_time):
                shoot_time = pygame.time.get_ticks()

            
        current_time = pygame.time.get_ticks()

        # print("current time {}, button pressed {}", current_time, shoot_time)

        ## moves the enemy
        
        
        for enemy in enemies:

            enemy.move(enemy_velocity)




        


main()
