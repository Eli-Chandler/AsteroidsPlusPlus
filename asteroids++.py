import arcade
import arcade.gui
from arcade.gui import UIManager

import random
import math
from datetime import datetime

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MOUSE_X = 0
MOUSE_Y = 0



USE_SPATIAL_HASHING = False


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

        self.dampers = 0
        self.damping = False

        self.max_fuel = 10
        self.fuel = 10

        self.velocity_radians = 0

        self.coins = 0

        self.last_shot = 3
        self.shoot_speed = 3
    def update(self, delta_time):

        self.last_shot += 1 * delta_time

        if self.at_base:
            self.fuel = self.max_fuel


        self.update_angle()

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
            print(self.fuel)
            self.delta_x += -self.thrusters * math.sin(self.radians)*delta_time
            self.delta_y += self.thrusters * math.cos(self.radians)*delta_time

        self.center_x += self.delta_x*delta_time
        self.center_y += self.delta_y*delta_time

    def update_angle(self):
        mouse_x_relative = MOUSE_X - SCREEN_WIDTH/2
        mouse_y_relative = MOUSE_Y - SCREEN_HEIGHT/2
        self.radians = math.atan2(mouse_y_relative, mouse_x_relative) - 1.5708

    def die(self):
        self.center_x = 0
        self.center_y = 0

        self.delta_x = 0
        self.delta_y = 0

        self.coins = 0

    def shoot(self, bullet_list):
        print(self.last_shot)
        if self.last_shot < self.shoot_speed:
            return

        delta_x = self.delta_x -100 * math.sin(self.radians)
        delta_y = self.delta_y + 100 * math.cos(self.radians)
        bullet_list.append(Bullet(self.center_x, self.center_y, delta_x, delta_y, self.angle, 2))
        self.last_shot = 0
        


ASTEROID_MIN_SIZE = 0.05
ASTEROID_MAX_SIZE = 0.4

ASTEROID_MAX_VELOCITY = 0.1
ASTEROID_MAX_ROTATION_SPEED = 1

class Bullet(arcade.Sprite):
    def __init__(self, center_x, center_y, delta_x, delta_y, angle, max_age):
        image = 'sprites/bomb.png'
        scale = 0.8
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
        if self.age >= self.max_age:
            self.kill()


class Asteroid(arcade.Sprite):
    def __init__(self, center_x, center_y, type='brown'):
        self.type = 'brown'
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
        image = 'sprites/explosion.png'
        scale = obj.scale
        super().__init__(image, scale)

        self.center_x = obj.center_x
        self.center_y = obj.center_y
        try:
            self.delta_x = obj.delta_x
        except: pass
        try:
            self.delta_y = obj.delta_y
        except: pass

        self.angle = obj.angle

        self.age = 0
        self.max_age = EXPLOSION_MAX_AGE
    def update(self, delta_time):
        self.center_x += self.delta_x*delta_time
        self.center_y += self.delta_y*delta_time

        self.age += 1 * delta_time
        if self.age >= self.max_age:
            self.kill()


class Coin(arcade.Sprite):
    def __init__(self, center_x, center_y, scale):
        image = 'sprites/coin/coin.png'
        super().__init__(image, scale)

        self.center_x = center_x
        self.center_y = center_y


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.bullet_list = None

        arcade.set_background_color(arcade.color.BLACK)

        self.asteroids_list = None

        self.rocket = None

        self.rocket_list = None

        self.asteroid_list = None

        self.explosion_list = None

        self.dead = None

        self.base = None

        self.coin_list = None

        self.existing_chunks = None

        self.BASE_ASTEROID_COUNT = None

        self.score = None

        self.ui_manager = UIManager()
    
    def setup(self):

        self.explosion_list = arcade.SpriteList()
        
        self.bullet_list = arcade.SpriteList()

        self.score = 0

        self.BASE_ASTEROID_COUNT = 100
        

        self.existing_chunks = []

        self.MAX_COINS = 1
        self.coin_list = arcade.SpriteList()

        self.rocket_list = arcade.SpriteList()
        self.rocket = Rocket('sprites/rocket/still.png')
        self.rocket_list.append(self.rocket)

        self.asteroid_list = arcade.SpriteList(use_spatial_hash=USE_SPATIAL_HASHING)

        self.base = arcade.Sprite('sprites/planets/earth.png', 1, center_x=0, center_y=0)

    def on_draw(self):
        


        arcade.start_render()

        self.bullet_list.draw()

        arcade.draw_line(self.rocket.center_x-50, self.rocket.center_y-50, self.base.center_x, self.base.center_y, arcade.color.PURPLE)

        self.coin_list.draw()
        self.base.draw()


        self.rocket.draw()

        self.asteroid_list.draw()

        arcade.draw_text(f'COINS: {self.rocket.coins}', self.rocket.center_x + SCREEN_WIDTH/2-100, self.rocket.center_y + SCREEN_HEIGHT/2-100, arcade.color.WHITE)

        arcade.draw_rectangle_filled(self.rocket.center_x, self.rocket.center_y - SCREEN_HEIGHT/2, SCREEN_WIDTH, 20, arcade.color.GRAY)



        arcade.draw_rectangle_filled(self.rocket.center_x - SCREEN_WIDTH + self.rocket.fuel * (SCREEN_WIDTH/self.rocket.max_fuel), self.rocket.center_y - SCREEN_HEIGHT/2, SCREEN_WIDTH, 20, arcade.color.GREEN)

        self.explosion_list.draw()

    def on_update(self, delta_time):
        
        for explosion in self.explosion_list:
            explosion.update(delta_time)

        for bullet in self.bullet_list:
            bullet.update(delta_time)

        self.coin_list.update()
        self.populate_coins()


        self.rocket.update(delta_time)

        self.asteroid_list.update()

        asteroid_hit_list = arcade.check_for_collision_with_list(self.rocket, self.asteroid_list)

        if asteroid_hit_list:
            if not self.rocket.invincible:
                self.rocket.die()

        base_hit_list = arcade.check_for_collision_with_list(self.base, self.asteroid_list)

        for asteroid in base_hit_list:
            asteroid.kill()

        at_base_check = arcade.check_for_collision(self.rocket, self.base)

        if at_base_check:
            self.rocket.at_base = True
        else:
            self.rocket.at_base = False


        coin_hit_list = arcade.check_for_collision_with_list(self.rocket, self.coin_list)

        for coin in coin_hit_list:
            coin.kill()
            self.rocket.coins += 1

        for bullet in self.bullet_list:
            bullet_hit_list = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
            if bullet_hit_list:
                bullet.kill()
                for asteroid in bullet_hit_list:
                    self.explosion_list.append(Explosion(asteroid))
                    asteroid.kill()


        self.populate_asteroids()

        arcade.set_viewport(self.rocket.center_x-SCREEN_WIDTH/2, self.rocket.center_x+SCREEN_WIDTH/2,
                            self.rocket.center_y-SCREEN_HEIGHT/2, self.rocket.center_y+SCREEN_HEIGHT/2)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.rocket.thrusting = True
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rocket.damping = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.rocket.shoot(self.bullet_list)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.rocket.thrusting = False
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rocket.damping = False

    def get_exterior_coords(self):

        # Get coordinates of screen edge
        left = self.rocket.center_x - SCREEN_WIDTH/2
        right = self.rocket.center_x + SCREEN_WIDTH/2

        top = self.rocket.center_y + SCREEN_HEIGHT/2
        bottom = self.rocket.center_y - SCREEN_HEIGHT/2

        return left, right, top, bottom

    def populate_asteroids(self):

        left, right, top, bottom = [int(i) for i in self.get_exterior_coords()]

        n = 0
        new = self.asteroid_list
        for asteroid in self.asteroid_list:
            if asteroid.center_x > right + 100 or asteroid.center_x < left - 100:
                new.pop(n)

            elif asteroid.center_y > top + 100 or asteroid.center_y < bottom - 100:
                new.pop(n)

            n += 1

        self.asteroid_list = new

        amount = self.BASE_ASTEROID_COUNT - len(self.asteroid_list)

        for i in range(amount):

            while True:
                center_x = random.randint(left-100, right+100)
                center_y = random.randint(bottom-100, top+100)

                if center_x > left-20 and center_x < right+20 and center_y > bottom-20 and center_y < top+20:
                    continue
                break
            self.asteroid_list.append(Asteroid(center_x, center_y))

    def populate_coins(self):
        chunk_x = round(self.rocket.center_x/1000)
        chunk_y = round(self.rocket.center_y/1000)

        nearby_chunks = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                nearby_chunks.append((chunk_x+i, chunk_y + j))
        for chunk in nearby_chunks:
            if chunk not in self.existing_chunks:
                self.existing_chunks.append(chunk)
                number_of_coins = self.MAX_COINS + int((chunk[0]**2 + chunk[1]**2)**0.5 /3)
                number_of_coins = random.randint(1, number_of_coins)
                print(number_of_coins)
                for i in range (0, number_of_coins):
                    coin_x = random.randint(chunk[0] * 1000, chunk[0] * 1000 + 1000)
                    coin_y = random.randint(chunk[1] * 1000, chunk[1] * 1000 + 1000)
                    self.coin_list.append(Coin(coin_x, coin_y, 0.05))




    def on_mouse_motion(self, x, y, dx, dy):
        global MOUSE_X, MOUSE_Y
        MOUSE_X = x
        MOUSE_Y = y


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, 'Asteroids++')
window.setup()
arcade.run()