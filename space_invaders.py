import pygame
from sys import exit
from random import randint 

pygame.init()

WIDTH, HEIGHT = 1500, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sam's Version of Space Invaders")

SPECIAL_SHIP = pygame.image.load('alien.png').convert_alpha()

REGULAR_SHIP = pygame.image.load('pixel.png').convert_alpha()

REGULAR_LASER = pygame.Surface((7, 40))

REGULAR_LASER.fill('red')

SPECIAL_LASER = pygame.Surface((7, 40))

SPECIAL_LASER.fill((173, 216, 230))

background = pygame.image.load('background.png').convert()

# laser_timer = pygame.USEREVENT + 1
#
# pygame.set_timer(laser_timer, 900)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('arcade-game.png').convert_alpha()

        self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT-150))

        self.last_shot = 0
        
        self.health = 100

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_s] and self.rect.bottom < 1000:
            self.rect.y += 5
        if keys[pygame.K_d] and self.rect.right < 1500:
            self.rect.x += 5
        if keys[pygame.K_SPACE]:
            if self.cooldown(current_time,self.last_shot):
                self.shoot()
                self.last_shot = pygame.time.get_ticks()

    def cooldown(self, current, last):
        return current - last>500

    def shoot(self):
        

        player_lasers.add(Laser(REGULAR_LASER, self.rect.midtop, -5))

    def collide(self):

        if collisions(player.sprite, enemies, True):
            self.health -= 25
        
        if collisions(player.sprite,enemy_lasers, True):
            self.health -= 20

    def update(self):
        self.player_input()
        self.collide()


class Enemies(pygame.sprite.Sprite):
    things = {
                'special': (SPECIAL_SHIP, SPECIAL_LASER),
                'regular': (REGULAR_SHIP, REGULAR_LASER)
                }
    def __init__(self, model, x, y):
        super().__init__()
        self.model = model
        self.image = self.things[self.model][0]
        self.rect = self.image.get_rect(center = (x, y))

        self.last_shot = 0
        

    def update(self):
        self.rect.y += 3


        if self.cooldown(current_time, self.last_shot) and self.inFrame():
            self.shoot()
            self.last_shot= pygame.time.get_ticks()
            

        self.destroy()
        self.collide()

    def cooldown(self, current, last):
        return current - last>4000

    def inFrame(self):
        if self.rect.top > 0:
            return True

    def shoot(self):


        enemy_lasers.add(Laser(self.things[self.model][1], self.rect.midbottom, 5))


    def collide(self):
        pygame.sprite.groupcollide(player_lasers, enemies, True, True)


    def destroy(self):
        if self.rect.top>HEIGHT:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, image, point, velo):
        super().__init__()
        self.velo = velo
        self.image = image
        self.rect= self.image.get_rect(center = point)

    def move(self):
        self.rect.y += self.velo

    def update(self):

        self.move()


def collisions(sprite, group, doKill):
    if pygame.sprite.spritecollide(sprite, group, doKill):
        return True
    else: return False


player = pygame.sprite.GroupSingle()
player.add(Player())

enemies = pygame.sprite.Group()

enemy_lasers = pygame.sprite.Group()

player_lasers = pygame.sprite.Group()


clock = pygame.time.Clock()

FPS = 60

level = 0
wavelength = 0
last_shot = 0

# enemies.add(Enemies('special', 500, 500))

while True:

    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            pygame.quit()
            exit()


    if len(enemies) == 0:
        print(level)
        level += 1
        wavelength += 5
        for i in range(wavelength):
            if randint(0, 5):
                enemies.add(Enemies('regular',randint(0, 1500), randint(-4000, 0)))
            else:
                enemies.add(Enemies('special',randint(0, 1500), randint(-4000, 0)))
                

        
    current_time = pygame.time.get_ticks()


    player.draw(screen)

    player.update()


    enemies.draw(screen)
    enemies.update()

    enemy_lasers.draw(screen)
    enemy_lasers.update()

    player_lasers.draw(screen)
    player_lasers.update()




    clock.tick(FPS)


    pygame.display.update()
