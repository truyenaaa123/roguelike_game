from source.player import *
import pygame
from source.settings import *
from source.support import *
from source.entity import *
import math
import random

class Ability(Entity):
    def __init__(self, player, PATH, bullet_sprite, size, corlorkey, scale ):
        super().__init__(bullet_sprite)
        self.player_rect = player.rect.copy()
        self.path = PATH
        self.image = import_image_sheet([PATH], size, corlorkey, scale)[0]
        self.rect = self.image.get_rect(topleft = self.player_rect.center)
        self.hitbox = self.rect
        self.obstacle_sprites = player.obstacle_sprites

            # Xóa viên đoạn khi đi quá xa player
    def delete(self):
        distance = math.sqrt((self.player_rect.centerx - self.rect.centerx) ** 2 + (self.player_rect.centery - self.rect.centery) ** 2)
        if distance > SCREEN_WIDTH + 500:
            self.kill()

class Bullet(Ability):
    def __init__(self, player, PATH, bullet_sprite):
        super().__init__(player, PATH, bullet_sprite, (359, 117), (255,255,255), 0.15 )
        self.shoot(player.status)
        self.speed = 20
        self.damage = 10

    # Bắn 
    def shoot(self, status):
        if 'up' in status:
            self.direction.y = -1
            self.image = import_image_sheet([self.path], (359, 117), (255,255,255), 0.15, 270)[0]
            self.player_rect.centery -= 50

        elif 'down' in status:
            self.direction.y = 1
            self.image = import_image_sheet([self.path], (359, 117), (255,255,255), 0.15, 90)[0]
            self.player_rect.centery += 20

        if 'left' in status:
            self.direction.x = -1
            self.player_rect.centerx -= 75
        elif 'right' in status:
            self.direction.x = 1
            self.image = import_image_sheet([self.path], (359, 117), (255,255,255), 0.15, 180)[0]
            self.player_rect.centerx += 20

    def update(self):
        self.move(self.speed)
        self.delete()

class FireBall(Ability):
    def __init__(self, player, path, fireball_sprite, direction):
        super().__init__(player, path, fireball_sprite, (1024,1024), (0,0,0), 0.05)
        self.sprite_type = 'fireball'
        self.player_rect = player.rect.copy()
        self.path = path
        self.direction = direction
        self.set_rotation()
        self.image = import_image_sheet([path], (1024,1024), (0,0,0), 0.05, rotation=self.rotation)[0]
        self.speed = 5
        self.damage = 1

    def set_rotation(self):
        if self.direction == (0,1):
            self.rotation = 45
        elif self.direction == (1,1):
            self.rotation = 90
        elif self.direction == (1,0):
            self.rotation = 135
        elif self.direction == (1,-1):
            self.rotation = 180
        elif self.direction == (0,-1):
            self.rotation = 225
        elif self.direction == (-1,-1):
            self.rotation = 270
        elif self.direction == (-1,0):
            self.rotation = 315
        else: self.rotation = 0

    def update(self):
        self.move(self.speed)
        self.delete()

class Boomerang(Ability):
    def __init__(self, player, path, boomerang_sprite, direction):
        super().__init__(player, path, boomerang_sprite,(331,311), (0,0,0), 0.2)
        self.direction = direction
        self.sprite_type = 'boomerang'
        self.player_rect = player.rect.copy()
        self.path = path
        self.load_animation()
        self.speed = 10
        self.damage = 50
        self.animation_speed =0.3

    def load_animation(self):
        self.animation = []
        for i in range(1,17):
            self.animation.append(import_image_sheet([self.path], (331,311), (0,0,0), 0.1, rotation=22.5*i)[0])

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center= self.hitbox.center)

    def update(self):
        self.move(self.speed)
        self.delete()
        self.animate()