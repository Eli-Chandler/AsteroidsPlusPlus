import arcade
import random
import math
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MOUSE_X = 0
MOUSE_Y = 0

CHUNK_SIZE = 500
BASE_ASTEROID_COUNT = 100

USE_SPATIAL_HASHING = False

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
    def __init__(self, center_x, center_y):
        image = 'sprites/asteroids/brown_asteroid.png'
        scale = 1
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

        self.rocket_list = None

        self.asteroid_list = None

        self.dead = None

        self.base = None
    def setup(self):

        self.dead = False

        self.rocket_list = arcade.SpriteList()

        self.rocket = Rocket('sprites/rocket/still.png')

        self.rocket_list.append(self.rocket)


        self.asteroid_list = arcade.SpriteList(use_spatial_hash=USE_SPATIAL_HASHING)

        self.base = arcade.create_rectangle_filled(0, 0, 100, 100, arcade.color.PINK_LAVENDER)

        for i in range(0):
            asteroid_x = random.randint(self.rocket.center_x-SCREEN_WIDTH/2, self.rocket.center_x+SCREEN_WIDTH/2)
            asteroid_y = random.randint(self.rocket.center_y-SCREEN_HEIGHT/2, self.rocket.center_y+SCREEN_HEIGHT/2)

            asteroid = Asteroid(asteroid_x , asteroid_y)
            self.asteroid_list.append(asteroid)




    def on_draw(self):
        

        arcade.start_render()
        self.base.draw()

        self.rocket.draw()

        self.asteroid_list.draw()

        


        #arcade.draw_circle_filled(300, 300, 10, arcade.color.AERO_BLUE)

        


    def on_update(self, delta_time):
        self.rocket.update(delta_time)

        self.asteroid_list.update()

        asteroid_hit_list = arcade.check_for_collision_with_list(self.rocket, self.asteroid_list)

        if asteroid_hit_list:
            self.rocket.center_x = 0
            self.rocket.center_y = 0

        base_hit_list = arcade.check_for_collision_with_list(self.base, self.asteroid_list)

        for asteroid in base_hit_list:
            asteroid.kill()

        self.populate_asteroids()

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

        amount = BASE_ASTEROID_COUNT - len(self.asteroid_list)

        for i in range(amount):
            
            while True:
                center_x = random.randint(left-100, right+100)
                center_y = random.randint(bottom-100, top+100)

                if center_x > left-20 and center_x < right+20 and center_y > bottom-20 and center_y < top+20:
                    continue
                break
            self.asteroid_list.append(Asteroid(center_x, center_y))
        






    def on_mouse_motion(self, x, y, dx, dy):
        global MOUSE_X, MOUSE_Y
        MOUSE_X = x
        MOUSE_Y = y

window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, 'Asteroids++')
window.setup()
arcade.run()