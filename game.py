import arcade
from arcade.application import MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HEIGHT/2
# INITIAL_D = 'Takumi'
INITIAL_THRUST = 1
class Rocket():
    def __init__(self, x, y, thrust):
        #Movement variables
        self.x = x
        self.y = y
        self.thrust_y = 0
        self.thrust_x = 0

        #force variables
        self.thrust = thrust
        self.damping_force = 0

        #active variables
        self.thrusters = False
        self.dampers = False

        #Upgrade variables

rocket = Rocket(0, 0, INITIAL_THRUST)

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
mouse = Mouse()

class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK) #Sets background color of window

        self.ax = 100
        self.ay = 100
        self.clicked = False

    def on_draw(self):
        arcade.start_render()
        arcade.draw_circle_filled(CENTER_X, CENTER_Y, 25, arcade.color.AFRICAN_VIOLET)

        arcade.draw_circle_filled(CENTER_X-rocket.x, CENTER_Y-rocket.y, 10, arcade.color.GRAY)

    def on_update(self, delta_time):
        rocket.x += rocket.thrust_x*delta_time
        rocket.y += rocket.thrust_y*delta_time

        if rocket.thrusters:
            xr = mouse.x-CENTER_X
            yr = mouse.y-CENTER_Y
        
            hypr = (xr**2 + yr**2)**0.5

            rocket.thrust_x += (xr/hypr)*rocket.thrust
            rocket.thrust_y += (yr/hypr)*rocket.thrust
    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            rocket.thrusters = True
        if button == arcade.MOUSE_BUTTON_RIGHT:
            rocket.dampers = True
            
        

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            rocket.thrusters = False
        if button == arcade.MOUSE_BUTTON_RIGHT:
            rocket.dampers = False
       
    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        mouse.x = x
        mouse.y = y
        


        



MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, 'My game window')
arcade.run()