import pygame
from source.settings import *
from source.support import *
from source.entity import *
from source.ability import *
import math
import random

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, attack_sprites, PATH):
        super().__init__(groups)
        self.image = pygame.image.load(PATH).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.bullet_group = pygame.sprite.Group()
        self.attack_sprites = attack_sprites
        self.is_levelup = False

        # timer
        self.end_time = 60 * 60 *10
        self.current_time = 0
        self.current_time_string = "0:00"

        # item
        self.maget_active = False
        self.magnet_active_time = pygame.time.get_ticks()
        self.boom_active = False
        self.upgrade_select = ""
        self.vaccum_item = 100

        # animation
        self.import_player_assets()
        self.status = 'down'

        # chỉ số
        self.stats = player_data.copy()
        self.damage = self.stats['damage']
        self.health = self.stats['health']
        self.exp = 0
        self.level = 0
        self.speed = self.stats['speed']

        # item
        self.attack_speed =  20
        self.frame_index_as = 0
        self.frame_index_asfb = 0
        self.fireball_cooldown = 60 * 4
        self.num_fireball = 0
        self.frame_index_asbmr = 120
        self.boomerang_cooldown = 60 * 4
        self.num_boomerang = 0

        self.obstacle_sprites =  obstacle_sprites
        self.frame_index_exp = 0
        self.exp_speed = 30
 
    # load animation từ sheet 
    def import_player_assets(self):
        character_path = 'texture/arachne.png'
        self.animation = {'up': [],'right': [],'down': [],'left': [],
                          'up_idle': [],'down_idle': [],'left_idle': [],'right_idle': []}
        #up,right,down,left
        count = -3
        surface_list = import_image_sheet([character_path], (48, 64), (0,0,0), 1.2)
        for animation in self.animation.keys():
            count += 3
            if 'idle' in animation:
                self.animation[animation].append(self.animation[animation.replace("_idle", "")][0])
            else: 
                self.animation[animation] = surface_list[count:count+3]
        # print(self.animation)
    
    # Di chuyển nhân vật bằng 4 nút
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else: self.direction.y =0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else: self.direction.x =0

    # Xác định trạng thái đứng yên và di chuyển
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status += '_idle'
    
    # Animation của player
    def animate(self):
        animation = self.animation[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center= self.hitbox.center)

    # Tạo viên đạn
    def create_bullet(self):
        self.frame_index_as += 1
        if self.frame_index_as >= self.attack_speed:
            self.frame_index_as = 0
            bullet_sprite = self.groups() + [self.attack_sprites]
            sound = pygame.mixer.Sound("sound/spell.mp3")
            sound.set_volume(0.1)
            sound.play()
            Bullet(self, BULLET_PATH, bullet_sprite)

    # Tạo Fire Ball:
    def create_fireball(self):
        self.frame_index_asfb += 1
        if self.frame_index_asfb >= self.fireball_cooldown:
            self.frame_index_asfb = 0
            fireball_prite = self.groups() + [self.attack_sprites]
            direction_list = [pygame.math.Vector2(x,y) for x in [-1,0,1] for y in [-1,0,1] if not(x ==y and x ==0)]
            direction = random.sample(direction_list, self.num_fireball)   
            for d in direction:         
                FireBall(self, FIREBALL_PATH, fireball_prite, d)
    
    # Tạo boomberang
    def create_boomerang(self):
        self.frame_index_asbmr += 1
        if self.frame_index_asbmr >= self.boomerang_cooldown:
            self.frame_index_asbmr = 0
            boomerang_prite = self.groups() + [self.attack_sprites]
            direction_list = [pygame.math.Vector2(x,y) for x in [-1,0,1] for y in [-1,0,1] if not(x ==y and x ==0)]
            direction = random.sample(direction_list, self.num_boomerang) 
            for d in direction:         
                Boomerang(self, BOOMERANG_PATH, boomerang_prite, d)

    # Tùy chỉnh tốc độ tăng cấp
    def level_up(self):
        self.frame_index_exp += 1
        if self.frame_index_exp >= self.exp_speed:
            self.frame_index_exp = 0
            self.stats['exp'] = player_data['exp'] + self.level * 40
            if self.exp >= self.stats['exp']:
                self.exp -= self.stats['exp']
                self.level += 1
                self.is_levelup = True

    # Nâng cấp
    def upgrade(self):
        if self.upgrade_select == 'fireball':
            self.num_fireball += skill_data[self.upgrade_select]
        elif self.upgrade_select == 'boomerang':
            self.num_boomerang += skill_data[self.upgrade_select]
        elif self.upgrade_select == 'damage':
            self.damage += skill_data[self.upgrade_select]
        elif self.upgrade_select == 'vaccum':
            self.vaccum_item += skill_data[self.upgrade_select]
        elif self.upgrade_select == 'health':
            self.stats['health'] += skill_data[self.upgrade_select]
        elif self.upgrade_select == 'speed':
            self.speed += skill_data[self.upgrade_select]
        elif self.upgrade_select == 'attack_speed':
            self.attack_speed -= skill_data[self.upgrade_select]

    # Timer
    def timer(self):
        if self.current_time >= self.end_time:
            print("end_game")
        else:
            self.current_time += 1
            if (self.current_time)//60 % 60 < 10:
                temp = "0" + str((self.current_time)//60 % 60 )
            else: temp = str((self.current_time)//60 % 60 )
            self.current_time_string = str(self.current_time//3600) + ":" + temp

    def update(self):
        self.create_bullet()
        self.create_fireball()
        self.create_boomerang()
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.level_up()
        self.timer()
        # print(self.num_boomerang)

