# main.py
import pygame

from game import Game
from settings import WIDTH, HEIGHT, FPS, IA_TRAINING, IA_PATH

from IA.IA import IA_DQN

def play():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()

    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        running = running and game.handle_input()
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

def training():
    IA = IA_DQN()
    IA.load_from_path(IA_PATH)
    #IA.load_from_path_expand("IA\\models\\IA1.pt", 16)

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    for i in range(IA_TRAINING):

        game = Game(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            running = running and game.IA_move(IA)
            game.draw(i, IA.steps)

            pygame.display.flip()
            clock.tick(FPS)
        IA.save_to_path(IA_PATH)
    pygame.quit()

def main():
    training()
    #play()
    
    print("2048 ended succefull")
    

if __name__ == "__main__":
    main()