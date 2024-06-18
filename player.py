import pygame, math
from vec2 import vec2
from rigidbody import RigidBody
from config import config

class Player(RigidBody):
    def __init__(self, game, starting_pos):
        super().__init__(starting_pos, 6, 8)
        self.game = game
        self.data = config['jumpers']['madeline']
        self.move_input = vec2(0, 0)

        self.grounded = False

        # JUMP
        self.jump_to_consume = False
        self.buffered_jump_usable = True
        self.ended_jump_early = False
        self.coyote_usable = True
        self.time_jump_was_pressed = 0.0
        self.can_use_coyote = True

        self.has_buffered_jump = False

        # TIME
        self.time_alive = 0

    def execute_jump(self):
        self.ended_jump_early = False
        self.time_jump_was_pressed = 0.0
        self.buffered_jump_usable = False
        self.coyote_usable = False
        self.velocity.y = self.data['jump_power']

    def handle_jump(self):
        """ self.has_buffered_jump = self.buffered_jump_usable and self.time_alive < self.time_jump_was_pressed + self.data['jump_buffer']
        #self.can_use_coyote = self.coyote_usable and not self.grounded and self.time_alive < 

        print(self.has_buffered_jump)

        if not self.grounded and not self.ended_jump_early and not self.game.inputs['up'] and self.velocity.y > 0:
            self.ended_jump_early = True

        if not self.jump_to_consume and not self.has_buffered_jump:
            return """

        if self.game.inputs['up'] and (self.grounded or self.can_use_coyote):
            self.execute_jump()
        
        self.jump_to_consume = False

    def handle_gravity(self, dt):
        if self.grounded:
            self.velocity.y = 0

        if self.grounded and self.velocity.y <= 0:
            self.velocity.y = self.data['grounding_force']
        else:
            in_air_gravity = self.data['fall_accel']
            #print(self.ended_jump_early)
            if self.ended_jump_early and self.velocity.y > 0:
                in_air_gravity *= self.data['jump_end_early_gravity_modifier']
            self.velocity.y = min(self.velocity.y + in_air_gravity * dt, self.data['max_fall_speed'])

    def handle_run(self, dt):
        target_speed = self.move_input.x * self.data['max_run_speed']

        if self.last_on_ground_time > 0:
            accel_rate = self.data['run_accel_amount'] if abs(target_speed) > 0.01 else self.data['run_deccel_amount']
        else:
            accel_rate = (self.data['run_accel_amount'] * self.data['accel_in_air'] if abs(target_speed) > 0.01 else self.data['run_deccel_amount'] * self.data['deccel_in_air'])

        if (self.data['do_conserve_momentum'] and abs(self.velocity.x) > abs(target_speed) and (self.velocity.x * target_speed) > 0 and abs(target_speed) > 0.01 and self.last_on_ground_time < 0):
            accel_rate = 0

        if self.last_on_ground_time > 0 and self.move_input.x == 0:
            amount = min(self.velocity.x, abs(self.friction))
            amount *= math.copysign(1.0, self.velocity.x)
            self.apply_force(vec2(amount, 0) * self.mass)

        speed_diff = target_speed - self.velocity.x
        movement = speed_diff * accel_rate
        self.velocity.x += movement * dt

    def move(self, tilemap):
        #COLLISIONS
        directions = {k: False for k in ['top', 'bottom', 'left', 'right']}

        self.position.x += self.velocity.x
        player_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if player_rect.colliderect(rect):
                if self.velocity.x > 0:
                    directions['right'] = True
                    player_rect.right = rect.left
                if self.velocity.x < 0:
                    directions['left'] = True
                    player_rect.left = rect.right
                self.position.x = player_rect.x
        
        self.position.y += self.velocity.y
        player_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if player_rect.colliderect(rect):
                if self.velocity.y > 0:
                    directions['bottom'] = True
                    player_rect.bottom = rect.top
                if self.velocity.y < 0:
                    directions['top'] = True
                    player_rect.top = rect.bottom
                self.position.y = player_rect.y

        self.grounded = directions['bottom']

    def turn(self):
        self.is_facing_right = not self.is_facing_right

    def check_facing_direction(self, is_moving_right):
        if is_moving_right != self.is_facing_right:
            self.turn()

    def update(self, tilemap, dt):
        self.time_alive += dt
        self.time_jump_was_pressed += dt
        
        self.handle_run(dt)
        self.handle_gravity(dt)
        self.handle_jump()
        self.move(tilemap)

        # CHANGE TO INPUTS MANAGER DONT PUT THIS IN PLAYER CLASS LOL
        if self.game.inputs['left']:
            self.move_input.x = -1
        elif self.game.inputs['right']:
            self.move_input.x = 1
        else:
            self.move_input.x = 0

        if self.move_input.x != 0:
            self.check_facing_direction(self.move_input.x > 0)
        self.debug()

    def render(self, surf):
        pygame.draw.rect(surf, 'red', self.rect())

    def debug(self):
        print('==================')
        print(f'Position: {self.position}')
        print(f'Velocity: {self.velocity}\n')
        print(f'Grounded: {self.grounded}')