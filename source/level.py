import pygame
import random
from source.settings import *
from source.tile import *
from source.player import *
from source.debug import debug
from source.ui import UI
from source.enemy import Enemy
from source.upgrade import *


class Level():
    def __init__(self) :
        # get display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        # attack sprite
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        # Chế độ challenger mode
        self.is_challenger_mode = False
        # sprite setup
        self.create_map()
        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player, self.is_challenger_mode)
        #Quay trờ lại màn hình chờ
        self.is_back = False

    # Tạo bản đồ lần đầu
    def create_map(self):
        self.player = Player((0, 0), [self.visible_sprites], self.obstacle_sprites,
                              self.attack_sprites, PLAYER_PATH)
        if self.is_challenger_mode:
            self.player.level = 57
            self.player.challenger_mode()
        enemy_pos = (self.player.rect.centerx+200, self.player.rect.centery +200)
        # self.enemy = Enemy(enemy_pos, [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, 'zombie')
        self.enemy = Enemy(enemy_pos, [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, 'bat')
        self.map = Spawner()           

    # Kiểm tra khi đạn trúng quái và sử dụng item    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite)
                        if hasattr(attack_sprite, 'sprite_type') and  (attack_sprite.sprite_type == 'boomerang'):
                            attack_sprite.direction = pygame.math.Vector2(random.random(), random.random())
                            attack_sprite.damage /= 2
                        elif hasattr(attack_sprite, 'sprite_type') and  (attack_sprite.sprite_type == 'fireball'):
                            pass
                        else: attack_sprite.kill()
                        if target_sprite.health <= 0:
                            target_sprite.drop_item([self.visible_sprites], target_sprite.rect.center)
                            target_sprite.kill()

        # xóa toàn bộ quái khi nhặt boom
        if self.player.boom_active:
            for sprite in self.attackable_sprites:
                sprite.kill()
            self.player.boom_active = False
    
    def reset(self):
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.game_paused = False
        self.create_map()
        self.ui = UI()
        self.upgrade = Upgrade(self.player, self.is_challenger_mode)

    def toggle_menu(self):
        if self.player.health <= 0:
            self.game_paused = True
            font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            img = font.render("GAME OVER!", True, TEXT_COLOR)
            self.display_surface.blit(img, (SCREEN_WIDTH//2 - 60,SCREEN_HEIGHT//2 + 20))
            img = font.render("YOUR SCORE: "+self.player.current_time_string, True, TEXT_COLOR)
            self.display_surface.blit(img, (SCREEN_WIDTH//2 - 75,SCREEN_HEIGHT//2 + 40))
            img = font.render("PRESS SPACE TO PLAY AGAIN", True, TEXT_COLOR)
            self.display_surface.blit(img, (SCREEN_WIDTH//2 - 130,SCREEN_HEIGHT//2 + 60))
            img = font.render("PRESS Q KEY TO BACK MENU", True, TEXT_COLOR)
            self.display_surface.blit(img, (SCREEN_WIDTH//2 - 130,SCREEN_HEIGHT//2 + 80))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                self.reset()
            elif key[pygame.K_q]:
                self.is_back = True
                

        elif self.player.is_levelup and self.player.level <= 56:
            pygame.mixer.Sound("sound/levelup.mp3").play()
            self.game_paused = not self.game_paused
            self.player.is_levelup = False
        
        if self.upgrade.exit_upgrade:
            self.game_paused = not self.game_paused
            self.upgrade.exit_upgrade = False
            self.player.upgrade()

    def run(self):
        # process the game
        self.visible_sprites.custom_draw(self.player, self.map)
        self.ui.display(self.player)
        self.toggle_menu()
        if self.game_paused:
            if self.player.health > 0:
                self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.entity_update(self.player)
            self.player_attack_logic()
            self.map.zombie_spawner(self.player, self.attackable_sprites, self.visible_sprites, self.obstacle_sprites)

# Groups các sprites tùy chỉnh để Player luôn ở giữa màn hình và cơ chế bản đồ
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset_sprite = pygame.math.Vector2() # offset di chuyển các vật ngoài Player

    def custom_draw(self, player: Player, map: Spawner):
        # offset để chính map cho player ở giữa màn hình
        self.offset_sprite.x = player.rect.centerx - self.half_width
        self.offset_sprite.y = player.rect.centery - self.half_height
        
        # Tùy chỉnh để vẽ Tiles
        if map.first_rect_player.x == float('inf'):
            map.first_rect_player = self.offset_sprite.copy()
        else :
            deltax = map.first_rect_player.x - self.offset_sprite.x
            deltay = map.first_rect_player.y - self.offset_sprite.y
            map.set_limit(deltax, deltay)

        # Vẽ Tiles (map)
        for width in range(0, int(map.tiles.x)):
            for height in range(0, int(map.tiles.y)):
                # Tính tọa độ cho Tiles để player nằm ở trung tâm
                map.floor_rect.x = width * map.floor_width - map.tiles.x* map.floor_width//2 + (player.rect.centerx- player.rect.x)
                map.floor_rect.y = height * map.floor_height - map.tiles.y* map.floor_height//2 + (player.rect.centery- player.rect.y)
                # Điều chỉnh tọa độ theo direction player
                limit_xaxis_avg = map.limit_xaxis.x + map.limit_xaxis.y
                limit_yaxis_avg = map.limit_yaxis.x + map.limit_yaxis.y
                average_offset = pygame.math.Vector2(limit_xaxis_avg // 2, limit_yaxis_avg // 2)
                floor_offset_pos = map.floor_rect.topleft - self.offset_sprite - average_offset

                self.display_surface.blit(map.floor_surf, floor_offset_pos)
        # Vẽ các sprite
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.y):
            offset_pos = sprite.rect.topleft - self.offset_sprite
            self.display_surface.blit(sprite.image, offset_pos)

    def entity_update(self, player):
        entity_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and  (sprite.sprite_type == 'enemy' or sprite.sprite_type == 'gem')]
        for entity in entity_sprites:
            entity.private_player_update(player)
        


        