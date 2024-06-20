import pygame, sys
from pygame.locals import *
from config import config

class Input:
    def __init__(self, game):
        self.game = game

        self.states = {}

        self.input_mode = 'core'

        self.reset()

    def reset(self):
        for binding in config['input']:
            self.states[binding] = False

    def hold_reset(self):
        for binding in config['input']:
            if config['input'][binding]['toggle'] == 'hold':
                self.states[binding] = False

    def soft_reset(self):
        for binding in config['input']:
            if config['input'][binding]['toggle'] == 'press':
                self.states[binding] = False

    def update(self):
        self.soft_reset()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == 27):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                for binding in config['input']:
                    if set(config['input'][binding]['mode']).intersection({'all', self.input_mode}):
                        if config['input'][binding]['button'][0] == 'keyboard':
                            if config['input'][binding]['toggle'] in ['hold', 'press']:
                                if event.key in config['input'][binding]['button'][1]:
                                    self.states[binding] = True
            if event.type == KEYUP:
                for binding in config['input']:
                    if set(config['input'][binding]['mode']).intersection({'all', self.input_mode}):
                        if config['input'][binding]['button'][0] == 'keyboard':
                            if config['input'][binding]['toggle'] in ['hold', 'press']:
                                if event.key in config['input'][binding]['button'][1]:
                                    self.states[binding] = False