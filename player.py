import pygame, math
from vec2 import vec2
from rigidbody import RigidBody
from config import config

class Player(RigidBody):
    def __init__(self, game, starting_pos):
        super().__init__(starting_pos, 6, 8)
        self.game = game
        self.data = config['player']
        self.move_input = vec2(0, 0)

    def run(self, dt):
        # calculate the direction we want to move in and our desired velocity
        target_speed = self.move_input.x * self.data['max_run_speed']

        # gets an acceleration value based on if we are accelerating (including turning)
        # or trying to decelerate (stop) as well as applying a multiplier if we're airborn
        if self.last_on_ground_time > 0:
            accel_rate = self.data['run_accel_amount'] if abs(target_speed) > 0.01 else self.data['run_deccel_amount']
        else:
            accel_rate = (self.data['run_accel_amount'] * self.data['accel_in_air'] if abs(target_speed) > 0.01 else self.data['run_deccel_amount'] * self.data['deccel_in_air'])

        # we won't slow the player down if they are moving in their desired direction but at a greater speed than max_speed
        if (self.data['do_conserve_momentum'] and abs(self.velocity.x) > abs(target_speed) and (self.velocity.x * target_speed) > 0 and abs(target_speed) > 0.01 and self.last_on_ground_time < 0):
            # conserve the current momentum
            accel_rate = 0

        # friction
        if self.last_on_ground_time > 0 and self.move_input.x == 0:
            amount = min(self.velocity.x, abs(self.friction))
            amount *= math.copysign(1.0, self.velocity.x)
            self.apply_force(vec2(amount, 0) * self.mass)

        # calculate the difference between target velocity and current velocity
        speed_diff = target_speed - self.velocity.x

        # calculate force along x-axis to apply to the character
        movement = speed_diff * accel_rate

        # apply to position
        self.velocity.x += movement * dt
        self.position += self.velocity

        print(self.velocity.x)

    def turn(self):
        self.is_facing_right = not self.is_facing_right

    def check_facing_direction(self, is_moving_right):
        if is_moving_right != self.is_facing_right:
            self.turn()

    def update(self, dt):
        self.run(dt)

        if self.game.inputs['left']:
            self.move_input.x = -1
        elif self.game.inputs['right']:
            self.move_input.x = 1
        else:
            self.move_input.x = 0

        if self.move_input.x != 0:
            self.check_facing_direction(self.move_input.x > 0)

    def render(self, surf):
        pygame.draw.rect(surf, 'red', (self.position.x, self.position.y, self.width, self.height))