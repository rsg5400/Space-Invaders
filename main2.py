## Imports
import pygame
import os 
import time
import random

## creates the game
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
        

    def draw(self, velocity):
        screen.blit(self.img, (self.x, self.y))
        self.move(velocity)

    def move(self, velo):
        self.y -= velo

    def hit(self):
        pass



## class of a the main ship

class Ship():

    def __init__(self, xPosition, yPosition, health = 100):
        ## X and Y position
        self.x = xPosition
        self.y = yPosition 
        ## ship health
        self.health = health
        self.img = None 
        self.lasers = []



    def draw(self,laser_velo):
        ## draws the ship
        screen.blit(self.img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(laser_velo)

    def shoot(self, current, shot):

        if current-shot > 350:
            laser = Laser(self.x+self.get_height*.15, self.y - .8*self.get_height)

            self.lasers.append(laser)
            return True
        else:
            return False

        
    @property
    def get_height(self):
        return self.img.get_height()



class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = playerImg
        self.rect = self.img.get_rect()

    

class Enemy(Ship):
    def __init__(self):
        
        self.lasers=[]
        self.img = enemyImg
        self.rect = self.img.get_rect()
        self.x = random.randint(0, width-self.get_height)
        self.y = random.randint(0, 200)
        self.last_shot = 0
    def move(self,velo):
        self.y += velo
    def shoot(self, current_time):
        if current_time - self.last_shot > 1500:

            laser = Laser(self.x + self.get_height*.15, self.y + .8*self.get_height)
            self.lasers.append(laser)
            self.last_shot = pygame.time.get_ticks()
        

## function that tells if there is a collision between two objects or not
def collisions(ob1, ob2):
    return ob1.rect.colliderect(ob2.rect)






def main():
    ## variable that descides whether the function runs or not
    run = True
    FPS=60
    velocity = 5
    enemy_velocity = 2
    clock = pygame.time.Clock()
    ## list of enemy objects
    enemies = [Enemy() for i in range(6)]

    ## creates a player at specificied location
    player = Player(350,600)
    ## usef for cooldown time
    current_time = 0
    shoot_time = 0
    last_shot = 0
    ## draws everything in the screen
    def screen_update():
        ## fills the screen black
        screen.fill((0,0,0))

        player.draw(5)


        for enemy in enemies:

            enemy.draw(-5)
            


        pygame.display.update()

    while run:
        ## makes everything run in 60FPS
        clock.tick(FPS)
        screen_update()
        

        ## breaks while loop when the user quits the program    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        ## moves the ship around
        if keys[pygame.K_a] and player.x>=0:
            player.x -= velocity
        elif keys[pygame.K_d] and player.x <= width-player.get_height:
            player.x += velocity

        elif keys[pygame.K_w] and player.y >= 0:
            player.y -= velocity

        elif keys[pygame.K_s] and player.y <=height-player.get_height:
            player.y += velocity

        ## shoots lasers for player
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            if player.shoot(current_time, shoot_time):
                shoot_time = pygame.time.get_ticks()

            
        ## used for cooldown time
        current_time = pygame.time.get_ticks()

        
        
        ## moves the enemy
        for enemy in enemies:
            enemy.move(enemy_velocity)
            # print("current time {}, last_shot {}".format(current_time, last_shot))

            enemy.shoot(current_time)

            # enemy.last_shot = pygame.time.get_ticks()
            # print("current time {}, enemy last_shot {}".format(current_time, enemy.last_shot))



        


main()
