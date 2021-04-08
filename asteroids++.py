import arcade
import random
import math
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MOUSE_X = 0
MOUSE_Y = 0

CHUNK_SIZE = 500
CHUNK_ASTEROID_COUNT = 25

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
    def __init__(self, image, scale, center_x, center_y):
        super().__init__(image, scale)


        self.center_x = center_x
        self.center_y = center_y

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

        self.asteroid_list = None
    def setup(self):
        self.rocket = Rocket('sprites/rocket/still.png')

        self.asteroid_list = arcade.SpriteList()

        for i in range(100):
            asteroid_x = random.randint(self.rocket.center_x-SCREEN_WIDTH/2, self.rocket.center_x+SCREEN_WIDTH/2)
            asteroid_y = random.randint(self.rocket.center_y-SCREEN_HEIGHT/2, self.rocket.center_y+SCREEN_HEIGHT/2)
            print(asteroid_x, asteroid_y)

            asteroid = Asteroid('sprites/asteroids/Asteroid Brown.png', 1, asteroid_x , asteroid_y)
            self.asteroid_list.append(asteroid)




    def on_draw(self):
        arcade.start_render()
        self.rocket.draw()

        arcade.draw_circle_filled(300, 300, 10, arcade.color.AERO_BLUE)

        self.asteroid_list.draw()
    def on_update(self, delta_time):
        self.pop_asteroids()

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

    def pop_asteroids(self):
        n = 0
        to_pop = []
        for asteroid in self.asteroid_list:
            if asteroid.center_x > self.rocket.center_x + SCREEN_WIDTH/2 or asteroid.center_x < self.rocket.center_x - SCREEN_WIDTH/2:
                to_pop.append(n)


            elif asteroid.center_y > self.rocket.center_y + SCREEN_HEIGHT/2 or asteroid.center_y < self.rocket.center_y - SCREEN_HEIGHT/2:
                to_pop.append(n)
                
            n += 1

        for n in to_pop:
            self.asteroid_list.pop(n)
            print('Popping')

    def replace_asteroids(self):
        amount = CHUNK_ASTEROID_COUNT - len(self.asteroid_list)

        for i in range(amount):
            if random.randint(0, 1):
                center_x = random.randint(self.rocket.center_x + SCREEN_WIDTH/2, self.rocket.center_x + SCREEN_WIDTH/2 + 100)
            else: 
                center_x = random.randint(self.rocket.center_x - SCREEN_WIDTH/2, self.rocket.center_x - SCREEN_WIDTH/2 + 100)
            
            if random.randint(0, 1):
                center_y = random.randint(self.rocket.center_y + SCREEN_HEIGHT/2, self.rocket.center_y + SCREEN_HEIGHT/2 + 100)
            else: 
                center_x = random.randint(self.rocket.center_x - SCREEN_WIDTH/2, self.rocket.center_x - SCREEN_WIDTH/2 + 100)



    def on_mouse_motion(self, x, y, dx, dy):
        global MOUSE_X, MOUSE_Y
        MOUSE_X = x
        MOUSE_Y = y

window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, 'Asteroids++')
window.setup()
arcade.run()