import pygame
from source.settings import*
import random

class Upgrade():
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.attribute_nr = 3
        self.attribute_pool = list(skill_data.keys())*8
        self.attribute_pool_set = set(self.attribute_pool)
        self.random_skill_list = random.sample(list(self.attribute_pool_set), self.attribute_nr)

        # skill creation
        self.height = self.display_surface.get_size()[1] * 0.4
        self.width = self.display_surface.get_size()[0] // (self.attribute_nr + 1)
        self.create_skill()

        # selection system
        self. selection_index = 0
        self.selection_time = None
        self.can_move =True
        self.select_random = False
        self.exit_upgrade = False

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_d] and self.selection_index < self.attribute_nr-1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_a] and self.selection_index  > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.select_random = True
                self.exit_upgrade = True
            
    def selection_cooldown(self):
        if not self.can_move:
            current_time  = pygame.time.get_ticks()
            if current_time - self.selection_time >= 150:
                self.can_move = True

    def create_skill(self):
        self.skill_list = []

        for skill, index in enumerate(range(self.attribute_nr)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (skill*increment) + (increment - self.width)//2
            top = self.display_surface.get_size()[1] * 0.1

            skill = Skill(left,top,self.width,self.height, index, self.font)
            self.skill_list.append(skill)
    
    def update_attribute(self):
        if len(self.attribute_pool_set) < 3:
            self.attribute_nr = len(self.attribute_pool_set)
            # self.width = self.display_surface.get_size()[0] // (self.attribute_nr + 1)

    def random_skill(self):
        if self.select_random:
            self.player.upgrade_select = self.random_skill_list[self.selection_index]
            self.attribute_pool.remove(self.random_skill_list[self.selection_index])
            self.attribute_pool_set = set(self.attribute_pool)
            self.update_attribute()
            self.random_skill_list = random.sample(list(self.attribute_pool_set), self.attribute_nr)

    def display(self):
        self.update_attribute()
        self.input()
        self.selection_cooldown()
        self.random_skill()
        self.create_skill()

        for index, skill in enumerate(self.skill_list):
            name = self.random_skill_list[index]
            value = skill_data[name]
            skill.display(self.display_surface,self.selection_index, name, value)

        self.select_random = False

class Skill():
    def __init__(self,l,t,w,h,index,font: pygame.font.Font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
    
    def display_names(self,surface,name,selected):
        color = TEXT_COLOR  if selected else TEXT_COLOR_SELECTED
        title_surf = self.font.render(name.replace("_", " "), False, color)
        title_rect = title_surf.get_rect(center= self.rect.center)

        surface.blit(title_surf, title_rect)
    
    def display(self,surface,selection_num,name,value):
        if self.index == selection_num:
            pass
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.display_names(surface, name, self.index == selection_num)