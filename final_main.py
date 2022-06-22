##imports 
import pygame
from sys import exit
from random import randint 
import pdb

## initlizing pygame
pygame.init()

WIDTH, HEIGHT = 1500, 1000

## creates screen with dimesions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sam's Version of Space Invaders")

## loading images
SPECIAL_SHIP = pygame.image.load('alien.png').convert_alpha()

REGULAR_SHIP = pygame.image.load('pixel.png').convert_alpha()

REGULAR_LASER = pygame.Surface((7, 40))

REGULAR_LASER.fill('red')

SPECIAL_LASER = pygame.Surface((7, 40))

SPECIAL_LASER.fill((173, 216, 230))

healer_object = pygame.image.load('gas.png').convert_alpha()

health_height, health_width = 7, 60

bomb = pygame.image.load("/home/sam/Projects/Space-Invaders/bomb.png").convert_alpha()
background = pygame.image.load('background.jpg').convert_alpha()



class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('player.png').convert_alpha()

        self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT-150))

        self.last_shot = 0
        
        self.health = 100
        
        self.score = 0

        self.boost_time= 140



    ## takes payer input and moves or shoots 
    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 0:
            if self.boost() and self.boost_time>20:
                self.rect.y -= 10
            else: self.rect.y -= 5
        if keys[pygame.K_a] and self.rect.left > 0:
            if self.boost() and self.boost_time>20: 
                self.rect.x -= 10
            else: self.rect.x -= 5
        if keys[pygame.K_s] and self.rect.bottom < 1000:
            if self.boost() and self.boost_time>20: 
                self.rect.y += 10
            else: self.rect.y += 5
        if keys[pygame.K_d] and self.rect.right < 1500:
            if self.boost() and self.boost_time>20: 
                self.rect.x += 10
            else: self.rect.x += 5
        if keys[pygame.K_SPACE]:
            if self.cooldown(current_time,self.last_shot):
                self.shoot()
                self.last_shot = pygame.time.get_ticks()

        
        

    ## makes it so the player cannot spam lasers
    def cooldown(self, current, last):
        return current - last>500

    ## creates a instance of the laser group
    def shoot(self):
        
        player_lasers.add(Laser(REGULAR_LASER, self.rect.midtop, -5))

    ## checks to see if teh player collided with an enemy or enemy laser
    def collide(self):

        if collisions(player.sprite, enemies, True):
            self.health -= 25
            # pygame.transform.scale(health_bar, ((health_height, health_width-.25*health_width)))
            healthbar.sprite.damage(25)
        
        if collisions(player.sprite,enemy_lasers, True):
            self.health -= 10
            # pygame.transform.scale(health_bar, ((health_height, health_width-.1*health_width)))
            healthbar.sprite.damage(10)
            

        if collisions(player.sprite, healer, True):
            self.health = 100
            # pygame.transform.scale(health_bar, ((health_height, health_width)))
            healthbar.sprite.healthIncrease()

        if collisions(player.sprite, nuke, True):

            self.score+=int(len(enemies)*5/6*20 + 1/6*40)
            enemies.empty()
            enemy_lasers.empty()
            # pygame.transform.scale(health_bar, ((health_height, health_width)))

    ## deals with boost and can be used after a certain amount of time
    def boost(self):

        keys = pygame.key.get_pressed()
        ## limits amount of time that you can build up the boost
        if keys[pygame.K_b] and self.boost_time > 0:
            self.boost_time-=2
            boostbar.sprite.useBoost()
            return True
        else: 
            return False
        
    def limit_boost(self):
        if self.boost_time>=140:
            self.boost_time = 140
        elif self.boost_time < 0:
            self.boost_time = 0


        
    ## takes in all the functions
    def update(self):
        self.limit_boost()
        self.player_input()
        self.collide() 
        self.boost_time+=1


class healthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.height, self.width = 7, player.sprite.image.get_width()
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = (player.sprite.rect.centerx, player.sprite.rect.bottom+10))

    def damage(self, damage):
        if player.sprite.health >0:
            self.width -= (damage/100)*player.sprite.image.get_width() 
        else: 
            self.width = 0
        self.image=pygame.transform.scale(healthbar.sprite.image, ((self.width, self.height)))

    def healthIncrease(self):
        self.width = player.sprite.image.get_width()
    
        self.image = pygame.transform.scale(healthbar.sprite.image, ((self.width, self.height)))


    def update(self):
        
        self.rect = self.image.get_rect(bottomleft = (player.sprite.rect.left, player.sprite.rect.bottom+10))



class boostBar(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.height, self.width = 7, player.sprite.image.get_width()
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill('purple')
        self.rect = self.image.get_rect(center = (player.sprite.rect.centerx, player.sprite.rect.bottom+20))
    def useBoost(self):
        ## decrease boost proporitional to how much is used
        # if boost_time <= 20:
        #     self.image = pygame.transform.scale(boostbar.sprite.image, ((1, self.height)))
        # else:
        self.width -= 2/150*player.sprite.image.get_width()
        self.image = pygame.transform.scale(boostbar.sprite.image, ((self.width, self.height)))

    def storeBoost(self):
        if self.width >= player.sprite.image.get_width(): 
            self.width = player.sprite.image.get_width()
            self.image = pygame.transform.scale(boostbar.sprite.image, ((self.width, self.height)))

        else:
            self.width += 1/150*player.sprite.image.get_width()
            self.image = pygame.transform.scale(boostbar.sprite.image, ((self.width, self.height)))
    def update(self):
        self.storeBoost()

        self.rect = self.image.get_rect(bottomleft = (player.sprite.rect.left, player.sprite.rect.bottom+20))
        


class Enemies(pygame.sprite.Sprite):
    ## things {model: (ship, laser, score bonus, score bonus, velo of laser)}
    things = {
                'special': (SPECIAL_SHIP, SPECIAL_LASER, 40, 10),
                'regular': (REGULAR_SHIP, REGULAR_LASER, 20, 5)
                }
    def __init__(self, model, x, y):
        super().__init__()
        self.model = model
        self.score_bonus = self.things[self.model][2]
        self.image = self.things[self.model][0]
        self.rect = self.image.get_rect(center = (x, y))
        self.velo = self.things[self.model][3]

        self.last_shot = 0
        

    def update(self):
        self.rect.y += 3


        if self.cooldown(current_time, self.last_shot) and self.inFrame():
            self.shoot()
            self.last_shot= pygame.time.get_ticks()
            

        self.destroy()
        self.collide()

    ## makes sure there is a delay in the lasers being shot by the enemy
    def cooldown(self, current, last):
        return current - last>4000

    ## checks to see if the enemy has enetered the game
    ## used to see if the enemy can shoot lasers yet
    def inFrame(self):
        if self.rect.top > 0:
            return True

    ## creates an instance of the laser group
    def shoot(self):


        enemy_lasers.add(Laser(self.things[self.model][1], self.rect.midbottom, self.velo))

    ## checks to see if the player lasers hit the enemy
    def collide(self):
        if pygame.sprite.groupcollide(player_lasers, enemies, True, True):
            player.sprite.score += self.score_bonus


    ## deletes the instance from the enemy grouop when teh enemy leaves the frame
    def destroy(self):
        if self.rect.top>HEIGHT:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, image, point, velo):
        super().__init__()
        self.velo = velo
        self.image = image
        self.rect= self.image.get_rect(center = point)

    ## moves the laser at a certain velo depending of what type of enemy it is
    def move(self):
        self.rect.y += self.velo

    def update(self):

        self.move()
        self.destroy()

    ## destroys the laser once it exits the playing screen
    def destroy(self):
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()


## function to make code more readable in terms of collisions
def collisions(sprite, group, doKill):
    if pygame.sprite.spritecollide(sprite, group, doKill):
        return True
    else: return False

## object that when hit by player revives the player to full health
class HealthObject(pygame.sprite.Sprite):
    def __init__(self, x, y, adder = randint(0, 700), counter =0):
        super().__init__()
        self.image = healer_object
        self.rect = self.image.get_rect(center = (x, y))
        self.adder = adder
        self.counter = counter
    ## moves the healer object and makes it stop at a certain point for about 5 seconds
    ## 300/60FPS = 5seconds
    def move(self):
        if self.rect.y <= 200: self.rect.y += 5
        else:
            if self.rect.y <= self.adder + 200: self.rect.y += 5
            else:

                if self.counter <= 300:
                    self.counter +=1
                else:
                    self.kill()

    def update(self):
        self.move()


class Nuclear(pygame.sprite.Sprite):
    def __init__(self, x, y, adder = randint(0, 700), counter =0):
        super().__init__()
        self.image = bomb
        self.rect = self.image.get_rect(center = (x, y))
        self.adder = adder
        self.counter = counter

    def move(self):
        if self.rect.y <= 200: self.rect.y += 5
        else:
            if self.rect.y <= self.adder + 200: self.rect.y += 5
            else:

                if self.counter <= 300:
                    self.counter +=1
                else:
                    self.kill()

    def update(self):
        self.move()




## creates and adds the player single group and the player lasers group
player = pygame.sprite.GroupSingle()
player.add(Player())
player_lasers = pygame.sprite.Group()

## health bar group

# healthbar = pygame.sprite.GroupSingle()
# healthbar.add(healthBar())

## creates the enemy and enemy laser groups
enemies = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()

## creates the healer object group
healer = pygame.sprite.Group()

nuke = pygame.sprite.Group()

## used as a counter in the shooting stuff
clock = pygame.time.Clock()

##it updates this many times in one second
## it runs the code 60 times in one second basically
FPS = 60

level = 0
wavelength = 0
last_shot = 0

## descides whetether the game is till active
game_active = False 

font = pygame.font.SysFont(None, 40)
bigText = pygame.font.SysFont(None, 80)
smallText = pygame.font.SysFont(None, 30)

# enemies.add(Enemies('special', 500, 500))

while True:
    screen.blit(background, (0,0))

    if player.sprite.health <= 0: game_active = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not game_active:

            player.sprite.rect = player.sprite.image.get_rect(center = (WIDTH/2, HEIGHT-150))
            player.sprite.health = 100
            ## once the space bar is hit it turns the game back active
            healthbar = pygame.sprite.GroupSingle()
            healthbar.add(healthBar())

            boostbar = pygame.sprite.GroupSingle()
            boostbar.add(boostBar())
            game_active = True
            level = 0
            wavelength = 0
            
    if game_active:

        if len(enemies) == 0:
            level += 1
            nuke_counter=0
            health_counter=0
            
            level_text = font.render(f'Level: {level}', True, 'white')
            wavelength += 5
            for i in range(wavelength):
                if randint(0, 5):
                    enemies.add(Enemies('regular',randint(64, 1500-64), randint(-4000, -300)))
                else:
                    enemies.add(Enemies('special',randint(64, 1500-64), randint(-4000, -300)))

                if not randint(0, wavelength) and health_counter<2:

                    ## the adder is deterimes how far the health object goes down before it stops 

                    healer.add(HealthObject(randint(32, 1500-32), randint(-4000, 0)))
                    health_counter+=1
                if not randint(0, wavelength*2) and nuke_counter<1:
                
                    nuke.add(Nuclear(randint(64, 1500-64), randint(-4000, -1000)))
                    nuke_counter +=1
                    

                    

        screen.blit(level_text, (0, 0))
            

        current_time = pygame.time.get_ticks()

        ## draws and updates the classes

        player.draw(screen)

        player.update()


        enemies.draw(screen)
        enemies.update()

        enemy_lasers.draw(screen)
        enemy_lasers.update()

        player_lasers.draw(screen)
        player_lasers.update()

        healer.draw(screen)
        healer.update()

        nuke.draw(screen)
        nuke.update()

        healthbar.draw(screen)
        healthbar.update()

        boostbar.draw(screen)
        boostbar.update()


        screen.blit(font.render(f'score: {player.sprite.score}', True, 'white'), (0, 50))


        
    else:
        ## this runs when the game is not active
        enemies.empty()
        enemy_lasers.empty()
        player_lasers.empty()
        healer.empty()
        nuke.empty()
        
        if player.sprite.score > 0:
            screen.blit(bigText.render(f'score: {player.sprite.score}', True, 'white'), (600, 400))
        else:
            screen.blit(bigText.render("Space Invaders", True, 'red'), (530, 200))
            screen.blit(smallText.render("Creator: Sam Gallagher", True, 'white'), (600, 400))
            screen.blit(REGULAR_SHIP, (100, 300))
            screen.blit(smallText.render("- Hit for 20 Points", True, 'white'), (170, 332))
            screen.blit(SPECIAL_SHIP, (100, 400))
            screen.blit(smallText.render("- Hit for 40 Points", True, 'white'), (170, 432))
            screen.blit(healer_object, (100, 500))
            screen.blit(smallText.render("- Revives to full health", True, 'white'), (170, 532))
            screen.blit(bomb, (100, 600))
            screen.blit(smallText.render("- Eliminates all oponenets in wave", True, 'white'), (170, 632))
            
            screen.blit(font.render('W, A, S, D- To  move', True, 'white'), (1100, 300))
            screen.blit(font.render('Space- shoots lasers', True, 'white'),(1100,  400) )
            blitted_health = pygame.Surface((64, 7))
            blitted_health.fill('green')
            screen.blit(blitted_health, (1100, 500))
            screen.blit(smallText.render("- Health Bar", True, 'white'), (1170, 503))
            blitted_boost = pygame.Surface((64, 7))
            blitted_boost.fill('purple')
            screen.blit(blitted_boost, ((1100, 600)))
            screen.blit(smallText.render("- Boost Bar", True, 'white'), (1170, 603))



            
        
        screen.blit(font.render("Pres ENTER to Play", True, 'white'), (600, 650))

    ## sets the amount of time this code runs per second(60)
    clock.tick(FPS)
    ## this is used the update the background and everything that is not a group
    pygame.display.update()
