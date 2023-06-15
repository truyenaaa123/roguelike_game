import pygame
from source.settings import *
from source.player import *

class UI:
    def __init__(self):
        # cài đặt chung
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font_timer = pygame.font.Font(UI_FONT, UI_FONT_SIZE + 10)

        # bar
        self.health_bar_rect = pygame.Rect(10,34,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.exp_bar_rect = pygame.Rect(10,10,EXP_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect: pygame.Rect, color):
        # draw
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        # chỉnh thanh bar
        if current > max_amount:
            current = max_amount
        ratio = current / max_amount
        current_width = int(bg_rect.width * ratio)
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        # vẽ phần tùy chỉnh
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect,3)

    def show_level(self, level):
        text_surf = self.font.render("LV " + str(int(level)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 30
        y = 10
        text_rect = text_surf.get_rect(topright= (x,y))
        self.display_surface.blit(text_surf, text_rect)

    def show_timer(self, player:Player):
        text_surf = self.font_timer.render(player.current_time_string, False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] // 2
        y = 40
        text_rect = text_surf.get_rect(topright= (x,y))
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player: Player):
        self.show_bar(player.exp, player.stats['exp'], self.exp_bar_rect, EXP_COLOR)
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_timer(player)
        self.show_level(player.level)