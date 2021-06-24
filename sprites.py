import arcade
import math
import random

class Rocket(arcade.Sprite):
    def __init__(self, image):
        super().__init__(image)

        self.invincible = False
        self.at_base = False

        self.center_x = 0
        self.center_y = 0

        self.delta_x = 0
        self.delta_y = 0

        self.thrusters = 100
        self.thrusting = False

        self.recoil = 10

        self.dampers = 0
        self.damping = False

        self.max_fuel = 10
        self.fuel = 10

        self.velocity_radians = 0

        self.coins = 0

        self.last_shot = 3
        self.shoot_speed = 3

        self.bullet_list = arcade.SpriteList()
    def update(self, delta_time, mouse_x, mouse_y):

        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        self.last_shot += 1 * delta_time

        if self.at_base:
            self.fuel = self.max_fuel

        mouse_x_relative = mouse_x - current_screen_width/2
        mouse_y_relative = mouse_y - current_screen_height/2
        self.radians = math.atan2(mouse_y_relative, mouse_x_relative) - 1.5708

        self.velocity_radians = math.atan2(self.delta_y, self.delta_x) - 1.5708
        if self.damping:
            if self.delta_x > 0:
                self.delta_x += (self.delta_x * math.sin(self.velocity_radians)*delta_time) * self.dampers
            else:
                self.delta_x -= (self.delta_x * math.sin(self.velocity_radians)*delta_time) *self.dampers
            if self.delta_y > 0:
                self.delta_y -= (self.delta_y * math.cos(self.velocity_radians)*delta_time) * self.dampers
            else:
                self.delta_y += (self.delta_y * math.cos(self.velocity_radians)*delta_time) *self.dampers
        elif self.thrusting and self.fuel > 0:
            self.fuel -= 1 * delta_time
            self.delta_x += -self.thrusters * math.sin(self.radians)*delta_time
            self.delta_y += self.thrusters * math.cos(self.radians)*delta_time

        self.center_x += self.delta_x*delta_time
        self.center_y += self.delta_y*delta_time


    def die(self):
        self.center_x = 0
        self.center_y = 0

        self.delta_x = 0
        self.delta_y = 0

        self.coins = 0

    def shoot(self):



        print(self.last_shot)
        if self.last_shot < self.shoot_speed:
            return

        self.delta_x -= -self.recoil * math.sin(self.radians)
        self.delta_y -= self.recoil * math.cos(self.radians)
        
        delta_x = self.delta_x -100 * math.sin(self.radians)
        delta_y = self.delta_y + 100 * math.cos(self.radians)
        self.bullet_list.append(Bullet(self.center_x, self.center_y, delta_x, delta_y, self.angle, 2))
        self.last_shot = 0

class Marker(arcade.Sprite):
    def __init__(self, origin, target):
        image = 'sprites/edge marker.png'
        scale = 1
        super().__init__(image, scale)

        self.center_x = origin.center_x
        self.center_y = origin.center_y

        self.origin = origin
        self.target = target

    def update(self):

        

        self.center_x = self.origin.center_x
        self.center_y = self.origin.center_y



        relative_x = self.center_x - self.target.center_x
        relative_y = self.center_y - self.target.center_y

        self.radians = math.atan2(relative_y, relative_x) - 1.5708

    def check_visibility(self, screen_width, screen_height):
        

        if self.center_x + screen_width/2 < self.target.center_x or self.center_y + screen_height/2 < self.target.center_x:
            return True
        if self.center_x - screen_width/2 < self.target.center_x or self.center_y - screen_height/2 < self.target.center_x:
            
            return True
        return False

class Bullet(arcade.Sprite):
    def __init__(self, center_x, center_y, delta_x, delta_y, angle, max_age):
        image = 'sprites/bomb.png'
        scale = 0.3
        super().__init__(image, scale)

        self.center_x = center_x
        self.center_y = center_y
        
        self.delta_x = delta_x
        self.delta_y = delta_y

        self.angle = angle

        self.age = 0
        self.max_age = max_age

    def update(self, delta_time):
        self.center_x += self.delta_x*delta_time
        self.center_y += self.delta_y*delta_time

        self.age += 1 * delta_time



ASTEROID_MIN_SIZE = 0.05
ASTEROID_MAX_SIZE = 0.4
ASTEROID_MAX_VELOCITY = 0.1
ASTEROID_MAX_ROTATION_SPEED = 1
class Asteroid(arcade.Sprite):
    def __init__(self, center_x, center_y, type='brown'):
        self.type = type
        image = f'sprites/asteroids/{self.type}_asteroid.png'
        scale = 1
        super().__init__(image, scale)

        self.center_x = center_x
        self.center_y = center_y

        self.delta_x = random.uniform(-ASTEROID_MAX_VELOCITY,
                                      ASTEROID_MAX_VELOCITY)
        self.delta_y = random.uniform(-ASTEROID_MAX_VELOCITY,
                                      ASTEROID_MAX_VELOCITY)

        self.rotation_speed = random.uniform(
            -ASTEROID_MAX_ROTATION_SPEED, ASTEROID_MAX_ROTATION_SPEED)

        self.scale = random.uniform(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        self.angle = random.randint(0, 360)

    def update(self):
        self.angle += self.rotation_speed
        self.center_x += self.delta_x
        self.center_y += self.delta_y

    def shot(self):
        if self.type == 'brown':
            pass
            # delete asteroid
        elif self.type == 'coin':
            pass
            # drop coins
        elif self.type == 'fuel':
            pass
            # drop fuel

EXPLOSION_MAX_AGE = 0.5
class Explosion(arcade.Sprite):
    def __init__(self, obj, EXPLOSION_MAX_AGE = EXPLOSION_MAX_AGE):
        scale = obj.scale
        image = 'sprites/explosion/explosion0.png'
        super().__init__(image,scale)

        self.center_x = obj.center_x
        self.center_y = obj.center_y
        try:
            self.delta_x = obj.delta_x
        except: pass
        try:
            self.delta_y = obj.delta_y
        except: pass

        self.angle = obj.angle


        self.current_texture = 0

        self.texture_list = [
            'explosion0.png',
            'explosion2.png',
            'explosion3.png',
            'explosion4.png',
            'explosion5.png',
            'explosion6.png',
        ]
        print(f'sprites/explosion/{self.texture_list[0]}')
        self.texture = arcade.sprite.load_texture(f'sprites/explosion/{self.texture_list[0]}')

        self.age = 0
        self.max_age = EXPLOSION_MAX_AGE

        self.anim_frame_time = self.max_age/len(self.texture_list)
        self.current_frame_time = self.anim_frame_time
    def update(self, delta_time):
        self.center_x += self.delta_x*delta_time
        self.center_y += self.delta_y*delta_time

        self.age += 1 * delta_time

        if self.age >= self.current_frame_time:
            try:
                self.texture = arcade.sprite.load_texture(f'sprites/explosion/{self.texture_list[self.current_texture]}')
            except:
                self.kill()
            self.current_texture += 1
            self.current_frame_time += self.anim_frame_time

class Coin(arcade.Sprite):
    def __init__(self, center_x, center_y, scale):
        image = 'sprites/coin/coin.png'
        super().__init__(image, scale)

        self.center_x = center_x
        self.center_y = center_y