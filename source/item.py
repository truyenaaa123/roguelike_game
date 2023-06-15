import pygame
from source.settings import *
from source.support import *
from source.entity import *
import math
from source.player import*

class Item(Entity):
    def __init__(self, groups, pos, obstacle_sprites, type_gem, path, size, colorkey, scale):
        super().__init__(groups)
        self.image = import_image_sheet([path], size, colorkey, scale)[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.sprite_type = 'gem'
        self.type_gem = type_gem
        self.value_gem = 10
        self.speed = 6
        self.obstacle_sprites = obstacle_sprites
    
    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > SCREEN_WIDTH//2 + 500:
            self.kill()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return distance, direction
    
    def pick(self, player:Player):
        current_time = pygame.time.get_ticks()
        self.speed = 3 + player.speed
        speed_magnet = 0
        if player.maget_active:
            self.distance_max = SCREEN_WIDTH//2
            speed_magnet = 10
        else: self.distance_max = player.vaccum_item
        
        distance, self.direction = self.get_player_distance_direction(player)
        if current_time - player.magnet_active_time >= 1200:
            player.maget_active = False
        if distance < 30:
            if (getattr(player, self.type_gem) <= player.stats[self.type_gem] - self.value_gem) or self.type_gem != 'health':
                setattr(player, self.type_gem, getattr(player, self.type_gem) + self.value_gem)
            else:
                setattr(player, self.type_gem, player.stats[self.type_gem])
            if self.type_gem == 'exp':
                pygame.mixer.Sound("sound/exp.mp3").play()
            self.kill()
        if distance < self.distance_max:
            self.move(self.speed + speed_magnet)

# Ngọc tăng exp spwan khi quái chết
class ExpGem(Item):
    def __init__(self, groups, pos, obstacle_sprites):
        super().__init__(groups, pos, obstacle_sprites,
                        'exp', EXP_PATH, (667,630), (0,0,0), 0.03)

    def private_player_update(self, player):
        self.pick(player)
    
    def update(self):
        pass

# Ngọc tăng máu spwan khi quái chết
class HealthGem(Item):
    def __init__(self, groups, pos, obstacle_sprites,
                 ):
        super().__init__(groups, pos, obstacle_sprites,
                         'health',HEALTH_PATH, (481, 417), (0,0,0), 0.06)
        self.value_gem = 200
    def private_player_update(self, player):
        self.pick(player)
    def update(self):
        pass

# Năm châm hút toàn bộ Ngọc spawn khi quái chết
class Magnet(Item):
    def __init__(self, groups, pos, obstacle_sprites,):
        super().__init__(groups, pos, obstacle_sprites,
                         '',MAGNET_PATH, (1920, 1833), (0,0,0), 0.02)
        self.active = False

    def pick(self, player:Player):
        distance, _ = self.get_player_distance_direction(player)
        if distance < 30:
            player.maget_active = True
            player.magnet_active_time = pygame.time.get_ticks()
            self.kill()

    def private_player_update(self, player):
        self.pick(player)
    def update(self):
        pass

# Boom nổ chết hết quái nhưng không để lại ngọc spawn khi quái chết
class Boom(Item):
    def __init__(self, groups, pos, obstacle_sprites,):
        super().__init__(groups, pos, obstacle_sprites,
                         '',BOOM_PATH, (1280,1024), (0,0,0), 0.04)
        self.active = False

    def pick(self, player:Player):
        distance, _ = self.get_player_distance_direction(player)
        if distance < 30:
            player.boom_active = True
            self.kill()

    def private_player_update(self, player):
        self.pick(player)
    def update(self):
        pass