import pygame
import toolbox
import math
import random
from powerup import PowerUp
from explosion import Explosion

class Enemy(pygame.sprite.Sprite):
    # Enemy constructor function
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        # Setting up the Enemy variables
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("../assets/Enemy_05.png")
        self.image_hurt = pygame.image.load("../assets/Enemy_05hurt.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion1.png"))
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion2.png"))
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion3.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0
        self.speed = 0.9
        self.health = 20
        self.hurt_timer = 0
        self.damage = 1
        self.obstacle_anger = 0
        self.obstacle_anger_max = 100
        self.powerup_drop_chance = 50 # out of 100

    def update(self, projectiles, crates, explosions):
        # Figure out the angle between the Enemy and the player
        self.angle = toolbox.angleBetweenPoints(self.x, self.y, self.player.x, self.player.y)

        # Move the Enemy in the direction it's facing
        angle_rads = math.radians(self.angle)
        self.x_move = math.cos(angle_rads) * self.speed
        self.y_move = -math.sin(angle_rads) * self.speed

        # Check to see if the Enemy is gonna run into a crate
        test_rect = self.rect
        new_x = self.x + self.x_move
        new_y = self.y + self.y_move

        test_rect.center = (new_x, self.y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_x = self.x
                self.getAngry(crate)

        test_rect.center = (self.x, new_y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_y = self.y
                self.getAngry(crate)
        
        self.x = new_x
        self.y = new_y
        self.rect.center = (self.x, self.y)

        # Check for collisions with explosions
        for explosion in explosions:
            if explosion.damage:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)
        
        # Check for collisions with projectiles
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)
                projectile.explode()

        if self.hurt_timer <= 0:
            image_to_rotate = self.image
        else:
            image_to_rotate = self.image_hurt
            self.hurt_timer -= 1
        
        image_to_draw, image_rect = toolbox.getRotatedImage(image_to_rotate, self.rect, self.angle)

        self.screen.blit(image_to_draw, image_rect)

    def getHit(self, damage):
        if damage:
            self.hurt_timer = 5
        self.x -= self.x_move * 20
        self.y -= self.y_move * 20
        self.health -= damage
        if self.health <= 0:
            # Set health very high so that self.kill only happens once
            self.health = 99999
            self.player.getScore(50)
            Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 0, False)

            if random.randint(0, 100) < self.powerup_drop_chance:
                PowerUp(self.screen, self.x, self.y)

            self.kill()

    def getAngry(self, crate):
        self.obstacle_anger += 1
        if self.obstacle_anger >= self.obstacle_anger_max:
            crate.getHit(self.damage)
            self.obstacle_anger = 0
