import pygame
from source.settings import *
from source.entity import Entity
from source.support import *
from source.player import *
from source.item import *
import random

class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, monster_name):
        # setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.display_surface = pygame.display.get_surface()

        # graphic
        self.monster_name = monster_name
        self.status = 'up'
        self.set_stats_graphic()
        self.import_graphics()
        self.image = self.animations[self.status][self.frame_index]

        # move
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-50)
        self.obstacle_sprites = obstacle_sprites

        # attack cooldown
        self.cooldown = 30
        self.frame_index_attack = 0
        self.is_attack = True

        #chỉ số
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.speed = monster_info['speed']
        self.damage = monster_info['damage']

    # chỉnh thông số load đồ họa
    def set_stats_graphic(self):
        if self.monster_name == 'zombie':
            self.stats_graphic = {'path': ['texture/zombie/Walk.png','texture/zombie/Attack.png' ],
                                  'number_action': [10, 8],
                                  'order_action': ['down', 'up', 'right', 'left','down_attack','up_attack','right_attack','left_attack'],
                                  'size':(32,32), 'colorkey':(0,0,0), 'scale':2.5,
                                  'limit_width_size':32, 'limit_height_size':0,
                                  'width_cut': 20, 'height_cut': 5}
        elif self.monster_name == 'bat':
            self.stats_graphic = {'path': ['texture/bat.png', 'texture/bat.png'],
                                  'number_action': [3, 3],
                                  'order_action': ['up', 'right', 'down', 'left','up_attack','right_attack','down_attack','left_attack'],
                                  'size':(48,64), 'colorkey':(0,0,0), 'scale':1.2,
                                  'limit_width_size':0, 'limit_height_size':0,
                                  'width_cut': 0, 'height_cut': 20}
        elif self.monster_name == 'snake':
            self.stats_graphic = {'path': ['texture/snake.png', 'texture/snake.png'],
                                  'number_action': [3, 3],
                                  'order_action': ['up', 'right', 'down', 'left','up_attack','right_attack','down_attack','left_attack'],
                                  'size':(64,64), 'colorkey':(0,0,0), 'scale':0.8,
                                  'limit_width_size':0, 'limit_height_size':0,
                                  'width_cut': 0, 'height_cut': 0}
        elif self.monster_name == 'dragon':
            self.stats_graphic = {'path': ['texture/dragon.png', 'texture/dragon.png'],
                                  'number_action': [3, 3],
                                  'order_action': ['up', 'right', 'down', 'left','up_attack','right_attack','down_attack','left_attack'],
                                  'size':(144,128), 'colorkey':(0,0,0), 'scale':1,
                                  'limit_width_size':0, 'limit_height_size':0,
                                  'width_cut': 0, 'height_cut': 0}
    

    #Lấy khoảng cách và hướng của quái với người chơi
    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > SCREEN_WIDTH//2 + 100:
            self.kill()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    # Cập nhật hướng mà quái phải chạy về phía người chơi
    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        collision = 45
        
        if distance <= collision:
            if 'attack' not in self.status:
                self.status += '_attack'
                self.animation_speed = 0.3
            self.frame_index_attack += 1
            if self.frame_index_attack >= self.cooldown:
                self.frame_index_attack =0
                self.is_attack = True
            if self.is_attack:
                player.health -= self.damage
                self.is_attack = False
        else:
            self.animation_speed = 0.15
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
            if (abs(self.direction[0]) > abs(self.direction[1])):
                if self.direction[0] > 0:
                    self.status = 'right'
                else: self.status = 'left'
            else:
                if self.direction[1] > 0:
                    self.status = 'down'
                else: self.status = 'up'

    # Quai tấn công thì đúng yên
    def actions(self,player):
        if 'attack' in self.status:
            self.direction = pygame.math.Vector2()
        else: 
            self.direction = self.get_player_distance_direction(player)[1]
            
    # upload và tùy chỉnh animation từ sheet
    def import_graphics(self):
        self.animations = {'up': [],'right': [],'down': [],'left': [],
                          'up_attack': [],'right_attack': [],'down_attack': [],'left_attack': []}
        surface_list = import_image_sheet(self.stats_graphic['path'],self.stats_graphic['size'], 
                                          self.stats_graphic['colorkey'],self.stats_graphic['scale'], 
                                        limit_width_size = self.stats_graphic['limit_width_size'],
                                        limit_height_size =self.stats_graphic['limit_height_size'],
                                        width_cut= self.stats_graphic['width_cut'], height_cut= self.stats_graphic['height_cut'])

        count_animate = 0
        count_action = 0
        index_number_option = 0
        for action in self.stats_graphic['order_action']:
            if count_action == 4:
                index_number_option = 1
            self.animations[action] = (surface_list[count_animate:count_animate+self.stats_graphic['number_action'][index_number_option]])
            count_animate += self.stats_graphic['number_action'][index_number_option]
            count_action += 1
    
    # animation cho quái
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    # trừ máu quái  
    def get_damage(self, player, attack_sprite):
        if hasattr(attack_sprite, 'sprite_type') and  (attack_sprite.sprite_type == 'fireball'):
            self.health -= (attack_sprite.damage + player.damage*0.1)
        else:
            self.health -= (player.damage + attack_sprite.damage)

    # quái chết rớt vật phẩm và tỉ lệ
    def drop_item(self, groups, pos):
        choices = ['exp_gem', 'heal_gem', 'magnet', 'boom']
        weights = [300, 5, 2, 1]
        result = random.choices(choices, weights, k=1)[0]
        if result == 'exp_gem':
            ExpGem(groups, pos, self.obstacle_sprites)
        elif result == 'heal_gem':
            HealthGem(groups, pos, self.obstacle_sprites)
        elif result == 'magnet':
            Magnet(groups, pos, self.obstacle_sprites)
        elif result == 'boom':
            Boom(groups, pos, self.obstacle_sprites)
        
    def update(self):
        self.move(self.speed)
        self.animate()
    
    def private_player_update(self, player):
        self.get_status(player)
        self.actions(player)







