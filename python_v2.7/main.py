#!/usr/bin/python
# coding: utf-8
import pygame

from game import Game


WIDTH, HEIGHT = 900, 600
FPS_LOCK = 60

def main():
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chaotic golf')

    game = Game(WIDTH, HEIGHT, FPS_LOCK)
    game.run(screen, fpsClock)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
