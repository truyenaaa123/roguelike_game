import pygame, sys
from source.settings import *
from source.level import Level

# Class của màn hình chính hiện thị cho người chơi
class Game:
    # khởi tạo game
    def __init__(self):
        # General setting
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Roguelike Game")

        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.fps = FPS
        self.level = Level()
        self.back = False
        

    def run_game(self):
        while self.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.display.blit(self.screen, (0,0))
            self.screen.fill((0,0,0))
            self.level.run()
            self.back = self.level.is_back
            if self.level.is_back:
                break
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game()
    game.run_game()