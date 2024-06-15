import pygame
from vec2 import vec2

class RigidBody:
    def __init__(self, pos, width, height, mass=1.0, elasticity=0.8, friction=0.05):
        self.position = vec2(pos)
        self.velocity = vec2(0, 0)
        self.acceleration = vec2(0, 0)
        self.width = width
        self.height = height
        self.mass = mass
        self.elasticity = elasticity
        self.friction = friction
        self.rect = pygame.Rect(pos[0], pos[1], width, height)

        # state parameters
        self._is_facing_right = True
        self._last_on_ground_time = 1.0
    
    def apply_force(self, force):
        self.acceleration += force / self.mass

    @property
    def is_facing_right(self):
        return self._is_facing_right

    @property
    def last_on_ground_time(self):
        return self._last_on_ground_time

    @is_facing_right.setter
    def is_facing_right(self, value):
        self._is_facing_right = value

    @last_on_ground_time.setter
    def last_on_ground_time(self, value):
        self._last_on_ground_time = value
