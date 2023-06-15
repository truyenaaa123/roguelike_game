import pygame, sys
from source.button import Button
import source.game
from source.settings import *


class Menu():
    def __init__(self):
        pygame.init()

        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Menu")
        self.BG = pygame.image.load("texture/Background.png")
        pygame.mixer.music.load("sound/menu.mp3")
        pygame.mixer.music.play(-1)
        self.is_menu_music = True

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("texture/font.ttf", size)

    def main_menu(self):
        while True:
            self.SCREEN.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(None, pos=(640, 250), 
                                text_input="NORMAL MODE", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(None, pos=(640, 400), 
                                text_input="CHALLENGER MODE", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(None, pos=(640, 550), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.music.load("sound/in_game.mp3")
                        pygame.mixer.music.play(-1)
                        self.is_menu_music = False
                        game_instance = source.game.Game()
                        game_instance.run_game()
                        if game_instance.level.is_back:
                            self.main_menu()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.music.load("sound/in_game.mp3")
                        pygame.mixer.music.play(-1)
                        self.is_menu_music = False
                        game_instance = source.game.Game()
                        game_instance.level.is_challenger_mode = True
                        game_instance.level.reset()
                        game_instance.run_game()
                        if game_instance.level.is_back:
                            self.main_menu()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            if not(self.is_menu_music):
                pygame.mixer.music.load("sound/menu.mp3")
                pygame.mixer.music.play(-1)
                self.is_menu_music = True
                    
            pygame.display.update()
