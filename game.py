import pygame, sys, os
from pygame.locals import *
from player import Player
from vec2 import vec2
from tilemap import Tilemap
from input import Input

# Constants
WIDTH = 320
HEIGHT = 180
FPS = 60
dt = 1/FPS
SCALE_RATIO = 3
BASE_RESOLUTION = (320, 180)
SCALED_RESOLUTION = (320 * SCALE_RATIO, 180 * SCALE_RATIO)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCALED_RESOLUTION)
        self.display = pygame.Surface(BASE_RESOLUTION)
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()

        self.input = Input(self)

        self.player = Player(self, (100, 0))
        self.floor = pygame.Rect(0, 120, WIDTH, 60)
        self.block = pygame.image.load('assets/temp.png')
        self.tilemap = Tilemap(self)
        self.tilemap.load('map.json')

    def update(self):
        self.input.update()

        self.tilemap.render(self.display)
        self.player.update(self.tilemap, dt)
        self.player.render(self.display)
        #pygame.draw.rect(self.display, 'black', self.floor)

        self.screen.blit(pygame.transform.scale(self.display, SCALED_RESOLUTION), (0, 0))
        self.clock.tick(FPS)
        self.display.fill((0, 147, 191))
        pygame.display.update()

    def run(self):
        while True:
            self.update()



game = Game()
game.run()