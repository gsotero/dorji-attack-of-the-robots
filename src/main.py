import pygame
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from crate import ExplosiveCrate
from explosion import Explosion
from powerup import PowerUp
from hud import HUD

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

background_image = pygame.image.load("../assets/BG_Sand.png")
# Make all the Sprite groups
playerGroup = pygame.sprite.Group()
projectilesGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
cratesGroup = pygame.sprite.Group()
explosionsGroup = pygame.sprite.Group()
powerupsGroup = pygame.sprite.Group()

# Put every Sprite class in a group
Player.containers = playerGroup
WaterBalloon.containers = projectilesGroup
Enemy.containers = enemiesGroup
Crate.containers = cratesGroup
Explosion.containers = explosionsGroup
PowerUp.containers = powerupsGroup

enemy_spawn_timer_max = 80
enemy_spawn_timer = 0

game_started = False

mr_player = Player(screen, game_width/2, game_height/2)

hud = HUD(screen, mr_player)

# StartGame function makes the game switch from main menu to in-game
def StartGame():
    global game_started
    game_started = True

# Make a bunch of crates
for i in range(0, 10):
    ExplosiveCrate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)
    Crate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)

# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(background_image, (0, 0))

    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                StartGame()
                break

    if game_started:
        # Deal with player input (figure out what keys are being pressed)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            mr_player.move(1, 0, cratesGroup)
        if keys[pygame.K_a]:
            mr_player.move(-1, 0, cratesGroup)
        if keys[pygame.K_w]:
            mr_player.move(0, -1, cratesGroup)
        if keys[pygame.K_s]:
            mr_player.move(0, 1, cratesGroup)
        if pygame.mouse.get_pressed()[0]:
            mr_player.shoot()
        if keys[pygame.K_SPACE]:
            mr_player.placeCrate()
        if pygame.mouse.get_pressed() [2]:
            mr_player.placeExplosiveCrate()

        # Make Enemy spawning happen
        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy(screen, 0, 0, mr_player)
            side_to_spawn = random.randint(0, 3) # 0 = top, 1 = bottom, 2 = left, 3 = right
            if side_to_spawn == 0:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = -new_enemy.image.get_height()
            elif side_to_spawn == 1:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = game_height + new_enemy.image.get_height()
            elif side_to_spawn == 2:
                new_enemy.x = -new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            elif side_to_spawn == 3:
                new_enemy.x = game_width + new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            enemy_spawn_timer = enemy_spawn_timer_max
    
        for powerup in powerupsGroup:
            powerup.update(mr_player)

        for explosion in explosionsGroup:
            explosion.update()

        for projectile in projectilesGroup:
            projectile.update()

        for enemy in enemiesGroup:
            enemy.update(projectilesGroup, cratesGroup, explosionsGroup)

        for crate in cratesGroup:
            crate.update(projectilesGroup, explosionsGroup)

        mr_player.update(enemiesGroup, explosionsGroup)

    hud.update()

    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("ATTACK OF THE ROBOTS fps: " + str(clock.get_fps()))
