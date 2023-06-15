import pygame
from source.settings import *
import math
import random
from source.enemy import *

class Spawner:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.tiles = pygame.math.Vector2() # số lượng tiles tối thiểu để lắp đầy map
        self.first_rect_player = pygame.math.Vector2((float('inf'), float('inf')))
        self.limit_xaxis = pygame.math.Vector2() # Chỉnh Tiles theo trục hoành
        self.limit_yaxis = pygame.math.Vector2() # Chỉnh Tiles theo trục tung

        self.floor_surf = pygame.image.load(FLOOR_PATH)
        self.floor_width = self.floor_surf.get_width()  
        self.floor_height = self.floor_surf.get_height()
        self.tiles.x = math.ceil(SCREEN_WIDTH / self.floor_width) + 2
        self.tiles.y = math.ceil(SCREEN_HEIGHT / self.floor_height) + 2
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        self.limit_xaxis.x = ((self.tiles.x -1) * self.floor_width - SCREEN_WIDTH)/2
        self.limit_xaxis.y = (SCREEN_WIDTH - self.tiles.x * self.floor_width)/2
        self.limit_yaxis.x = ((self.tiles.y -1) * self.floor_height - SCREEN_HEIGHT)/2
        self.limit_yaxis.y = (SCREEN_HEIGHT - self.tiles.y * self.floor_height)/2
    
    # Tạo giới hạn cho floor
    def set_limit(self, deltax, deltay):
        if deltay > self.limit_yaxis.x:
            self.limit_yaxis.x += self.floor_height
            self.limit_yaxis.y += self.floor_height
        if deltay < self.limit_yaxis.y:
            self.limit_yaxis.y -= self.floor_height
            self.limit_yaxis.x -= self.floor_height

        if deltax > self.limit_xaxis.x:
            self.limit_xaxis.x += self.floor_width
            self.limit_xaxis.y += self.floor_width
        if deltax < self.limit_xaxis.y:
            self.limit_xaxis.y -= self.floor_width
            self.limit_xaxis.x -= self.floor_width

    # Spawn ra quai
    def zombie_spawner(self, player:Player, attackable_sprites, visible_sprites, obstacle_sprites):
        enemy_spawn_num = min(int(player.level*2.5) + 15, 200)

        if len(attackable_sprites) <= enemy_spawn_num:
            top_max = player.rect.centery - SCREEN_HEIGHT//2 - 100
            bottom_max = player.rect.centery + SCREEN_HEIGHT//2+100
            left_max = player.rect.centerx - SCREEN_WIDTH//2 - 100
            right_max = player.rect.centerx + SCREEN_WIDTH//2+100
            top_min = player.rect.centery - SCREEN_HEIGHT//2 + 10
            bottom_min = player.rect.centery + SCREEN_HEIGHT//2 - 10
            left_min = player.rect.centerx - SCREEN_WIDTH//2 + 10
            right_min = player.rect.centerx + SCREEN_WIDTH//2 - 10

            state = random.choice([1,2,3])
            if state == 1:
                x_spawn = random.choice([random.randint(left_max, left_min), random.randint(right_min, right_max)])
                y_spawn = random.choice([random.randint(top_max, top_min), random.randint(bottom_min, bottom_max)])
            elif state == 2:
                x_spawn = random.randint(left_min, right_min)
                y_spawn = random.choice([random.randint(top_max, top_min), random.randint(bottom_min, bottom_max)])
            else:
                x_spawn = random.choice([random.randint(left_max, left_min), random.randint(right_min, right_max)])
                y_spawn = random.randint(top_min, bottom_min)
            # print(state)
            # print(x_spawn, y_spawn)
            if player.level <= 10:
                Enemy((x_spawn, y_spawn), [visible_sprites, attackable_sprites], obstacle_sprites, 'bat')
            elif player.level <= 20:
                Enemy((x_spawn, y_spawn), [visible_sprites, attackable_sprites], obstacle_sprites, 'zombie')
            elif player.level <= 30:
                Enemy((x_spawn, y_spawn), [visible_sprites, attackable_sprites], obstacle_sprites, 'snake')
            elif player.level <= 40:
                Enemy((x_spawn, y_spawn), [visible_sprites, attackable_sprites], obstacle_sprites, 'dragon')
            elif player.level <= 100:
                Enemy((x_spawn, y_spawn), [visible_sprites, attackable_sprites], obstacle_sprites, 'bat')
                Enemy((x_spawn, y_spawn), [visible_sprites, attackable_sprites], obstacle_sprites, 'zombie')
                Enemy((x_spawn, y_spawn), [visible_sprites, attackable_sprites], obstacle_sprites, 'snake')
                Enemy((x_spawn, y_spawn), [visible_sprites, attackable_sprites], obstacle_sprites, 'dragon')
