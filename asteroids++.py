import arcade
import random
import math
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MOUSE_X = 0
MOUSE_Y = 0

class Rocket(arcade.Sprite):
    def __init__(self, image):
        super().__init__(image)

        self.center_x = 0
        self.center_y = 0

        self.delta_x = 0
        self.delta_y = 0

        self.thrusters = 100
        self.thrusting = False

        self.dampers = 100
        self.damping = False

        self.velocity_radians = 0
    def update(self, delta_time): 

        self.update_angle()

        self.velocity_radians = math.atan2(self.delta_y, self.delta_x) - 1.5708


        if self.thrusting:
            self.delta_x += -self.thrusters * math.sin(self.radians)*delta_time
            self.delta_y += self.thrusters * math.cos(self.radians)*delta_time

        self.center_x += self.delta_x*delta_time
        self.center_y += self.delta_y*delta_time

    def update_angle(self):
        mouse_x_relative = MOUSE_X - SCREEN_WIDTH/2
        mouse_y_relative = MOUSE_Y - SCREEN_HEIGHT/2

        self.radians = math.atan2(mouse_y_relative, mouse_x_relative) - 1.5708


ASTEROID_MIN_SIZE = 0.05
ASTEROID_MAX_SIZE = 0.4

ASTEROID_MAX_VELOCITY = 0.1
ASTEROID_MAX_ROTATION_SPEED = 1
class Asteroid(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)


        self.center_x = 100
        self.center_y = 100

        self.delta_x = random.uniform(-ASTEROID_MAX_VELOCITY, ASTEROID_MAX_VELOCITY)
        self.delta_y = random.uniform(-ASTEROID_MAX_VELOCITY, ASTEROID_MAX_VELOCITY)

        self.rotation_speed = random.uniform(-ASTEROID_MAX_ROTATION_SPEED, ASTEROID_MAX_ROTATION_SPEED)

        self.scale = random.uniform(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        self.angle = random.randint(0, 360)

    def update(self):
        self.angle += self.rotation_speed
        self.center_x += self.delta_x
        self.center_y += self.delta_y


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.asteroids_list = None

        self.rocket = None
    def setup(self):
        self.asteroid_list = arcade.SpriteList()

        self.rocket = Rocket('sprites/rocket/still.png')


    def on_draw(self):
        arcade.start_render()
        self.rocket.draw()

        arcade.draw_circle_filled(300, 300, 10, arcade.color.AERO_BLUE)

        self.asteroid_list.draw()
    def on_update(self, delta_time):
        print(delta_time**-1)
        self.rocket.update(delta_time)

        self.asteroid_list.update()

        arcade.set_viewport(self.rocket.center_x-SCREEN_WIDTH/2, self.rocket.center_x+SCREEN_WIDTH/2, self.rocket.center_y-SCREEN_HEIGHT/2, self.rocket.center_y+SCREEN_HEIGHT/2)


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.rocket.thrusting = True
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rocket.damping = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.rocket.thrusting = False
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rocket.damping = False


    def on_mouse_motion(self, x, y, dx, dy):
        global MOUSE_X, MOUSE_Y
        MOUSE_X = x
        MOUSE_Y = y
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, 'Asteroids++')
window.setup()
arcade.run()