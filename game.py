import pygame, sys, os
from pygame.locals import *
from player import Player
from vec2 import vec2
from tilemap import Tilemap

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

        self.inputs = {
            "left": False,
            "right": False,
            "up": False,
            "down": False
        }

        self.player = Player(self, (100, 0))
        self.floor = pygame.Rect(0, 120, WIDTH, 60)
        self.block = pygame.image.load('assets/temp.png')
        self.tilemap = Tilemap(self)
        self.tilemap.load('map.json')

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == 27):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == 97:
                    self.inputs['left'] = True
                if event.key == 100:
                    self.inputs['right'] = True
                if event.key == 32:
                    self.inputs['up'] = True
                if event.key == 115:
                    self.inputs['down'] = True

            if event.type == KEYUP:
                if event.key == 97:
                    self.inputs['left'] = False
                if event.key == 100:
                    self.inputs['right'] = False
                if event.key == 32:
                    self.inputs['up'] = False
                if event.key == 115:
                    self.inputs['down'] = False

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