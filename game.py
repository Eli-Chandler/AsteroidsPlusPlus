import arcade
from arcade.application import MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT
import math
import random


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

SPRITE_SCALING = 1

CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HEIGHT/2
# INITIAL_D = 'Takumi'


class Rocket: #Creates rocket class
    def __init__(self):
        # Position variables
        self.x = CENTER_X #Symbolic X position of rocket (Rocket stays at 0, 0 and everything is moved around it)
        self.y = CENTER_Y #Symbolic Y position of rocket
        
        #Velocity Variables
        self.velocity_x = 0 #Current X velocity of rocket
        self.velocity_y = 0 #Current Y Velocity of rocket

        # active variables
        self.thrusters = False #If thrusters are enabled
        self.dampers = False #If dampers are enabled

        # Upgrade variables
        self.thrust = 1 #Acceleration of rocket (Default = 1)
        self.damping = 0 #Auto-decelleration of rocket (Default = 0)

rocket = Rocket()


class RocketSprite(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.center_x = CENTER_X
        self.center_y = CENTER_Y
    
    def update(self):
        mouse_x_relative = mouse.x-CENTER_X #Finds mouse x relative to position of rocket
        mouse_y_relative = mouse.y-CENTER_Y #Finds mouse y relative to position of rocket
        self.radians = math.atan2(mouse_y_relative, mouse_x_relative) - 1.5708 # Angle to Mouse position - 90 degrees in radians



class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0


mouse = Mouse()

STARTING_ASTEROID_AMOUNT = 10
ASTEROID_MIN_SIZE = 5
ASTEROID_MAX_SIZE = 75
ASTEROID_MAX_VELOCITY = 5

chunks = {}

def generate_asteroids():
    global chunks
    x = (int(round(rocket.x, -3)/1000))
    y = (int(round(rocket.y, -3)/1000))

    nearby_chunks = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            nearby_chunks.append((x+i, y+j))
    
    to_pop = []
    for chunk in chunks:
        if chunk not in nearby_chunks:
            to_pop.append(chunk)
            print('Popped', chunk)
    for chunk in to_pop:
        chunks.pop(chunk)




    
    for chunk in nearby_chunks:
        if chunk not in chunks:
            chunks[chunk] = []

            min_x = chunk[0] * 1000
            min_y = chunk[1] * 1000

            velocity_x = random.random()*ASTEROID_MAX_VELOCITY
            velocity_y = random.random()*ASTEROID_MAX_VELOCITY



            for i in range(STARTING_ASTEROID_AMOUNT):
                if random.randint(0, 1):
                    velocity_x = -velocity_x
                if random.randint(0, 1):
                    velocity_y = -velocity_y
                asteroid = {
                            'x':random.randint(min_x, min_x + 1000),
                            'y':random.randint(min_y, min_y + 1000),
                            'size':random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE),
                            'velocity_x':velocity_x,
                            'velocity_y':velocity_y
                }



                chunks[chunk].append(asteroid)
    





class MyGameWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK) # Sets background color of window to black

        self.ax = 100 # Test Asteroid X 
        self.ay = 100 # Test Asteroid Y

        self.rocket_list = None

        self.rocket_sprite = None

    def setup(self):
        self.rocket_list = arcade.SpriteList()

        self.rocket_sprite = RocketSprite('sprites/stillsprites/still.png', SPRITE_SCALING)

        self.center_x = CENTER_X
        self.center_y = CENTER_Y
        self.rocket_list.append(self.rocket_sprite)


    def on_draw(self):
        arcade.start_render()
        
        for chunk in chunks:
            for asteroid in chunks[chunk]:
                arcade.draw_circle_filled(asteroid['x']-rocket.x, asteroid['y']-rocket.y, asteroid['size'], arcade.color.GRAY)


        self.rocket_list.draw()

    def on_update(self, delta_time):
        generate_asteroids()
        
        for chunk in chunks:
            n = 0
            for asteroid in chunks[chunk]:
                chunks[chunk][n]['x'] += chunks[chunk][n]['velocity_x'] * delta_time
                chunks[chunk][n]['y'] += chunks[chunk][n]['velocity_y'] * delta_time
                n += 1
        #print(chunks[(1, 0)][0]['x'])


        
        rocket.x += rocket.velocity_x*delta_time #Delta time is the time between frames
        rocket.y += rocket.velocity_y*delta_time



        if rocket.thrusters:
            mouse_x_relative = mouse.x-CENTER_X #Finds mouse x relative to position of rocket
            mouse_y_relative = mouse.y-CENTER_Y #Finds mouse y relative to position of rocket

            hypr = (mouse_x_relative**2 + mouse_y_relative**2)**0.5 #Finds euclidean distance to rocket

            rocket.velocity_x += (mouse_x_relative/hypr)*rocket.thrust
            rocket.velocity_y += (mouse_y_relative/hypr)*rocket.thrust
        self.rocket_list.update()

        

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int): #When a mouse button is pressed this function is executed
        if button == arcade.MOUSE_BUTTON_LEFT: #If left mouse button is clicked thrusters are enabled - Rocket will start accelerating
            rocket.thrusters = True
        if button == arcade.MOUSE_BUTTON_RIGHT: #If Right mouse button is clicked dampers are enabled - Rocket will start decellerating
            rocket.dampers = True

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int): #When a mouse button is released this function is executed
        if button == arcade.MOUSE_BUTTON_LEFT: #If left mouse button is released thrusters are disabled - Rocket will stop accelerating
            rocket.thrusters = False
        if button == arcade.MOUSE_BUTTON_RIGHT: #If Right mouse button is clicked dampers are disabled - Rocket will stop decellerating
            rocket.dampers = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float): #When the mouse is moved this function is executed
        mouse.x = x 
        mouse.y = y


window = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, 'My game window')
window.setup()
arcade.run()
