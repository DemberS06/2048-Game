# main.py
import pygame

from game import Game
from settings import WIDTH, HEIGHT, FPS, IA_TRAINING

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
    for i in range(IA_TRAINING):
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

def main():
    #training()
    play()
    
    print("2048 ended succefull")
    

if __name__ == "__main__":
    main()