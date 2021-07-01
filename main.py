import arcade
import arcade.gui
from arcade.gui import UIManager

import random
import math
from datetime import datetime

import sprites
import buttons

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
current_screen_height = SCREEN_HEIGHT
current_screen_width = SCREEN_WIDTH

MOUSE_X = 0
MOUSE_Y = 0



USE_SPATIAL_HASHING = False

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

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

        self.score = None

        self.edge_marker = None

        self.fuel_progress_bar = None

        self.oxygen_progress_bar = None

        self.background = None
    
    def setup(self):

        self.fuel_progress_bar = sprites.ProgressBar(5, 'green')

        self.oxygen_progress_bar = sprites.ProgressBar(15, 'blue')


        arcade.set_background_color(arcade.color.BLACK)
        
        self.explosion_list = arcade.SpriteList()



        self.score = 0

        self.BASE_ASTEROID_COUNT = 100
        

        self.existing_chunks = []

        self.MAX_COINS = 1
        self.coin_list = arcade.SpriteList()

        self.rocket_list = arcade.SpriteList()
        self.rocket = sprites.Rocket('sprites/rocket/still.png')
        self.rocket_list.append(self.rocket)

        self.asteroid_list = arcade.SpriteList(use_spatial_hash=USE_SPATIAL_HASHING)

        self.base = arcade.Sprite('sprites/planets/earth.png', 1, center_x=0, center_y=0)

        self.edge_marker = sprites.Marker(self.rocket, self.base)

        self.background = sprites.Background(self.rocket)


    def on_draw(self):
        


        arcade.start_render()

        self.background.draw()

        
        self.rocket.bullet_list.draw()


        self.coin_list.draw()
        
        if not self.rocket.at_base and self.edge_marker.check_visibility(current_screen_width, current_screen_height):
            self.edge_marker.draw()

        self.base.draw()


        self.rocket.draw()

        self.asteroid_list.draw()


        self.explosion_list.draw()

        self.fuel_progress_bar.draw()
        self.oxygen_progress_bar.draw()

    def on_update(self, delta_time):

        self.explosion_list.update_animation()

        for explosion in self.explosion_list:
            explosion.update(delta_time)

        for bullet in self.rocket.bullet_list:
            bullet.update(delta_time)
            if bullet.age >= bullet.max_age:
                self.explosion_list.append(sprites.Explosion(bullet))
                bullet.kill()

        self.coin_list.update()
        self.populate_coins()


        self.rocket.update(delta_time, MOUSE_X, MOUSE_Y)

        self.asteroid_list.update()

        asteroid_hit_list = arcade.check_for_collision_with_list(self.rocket, self.asteroid_list)

        if asteroid_hit_list:
            if not self.rocket.invincible:
                self.setup()
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
            self.rocket.coins += 5

        for bullet in self.rocket.bullet_list:
            bullet_hit_list = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
            if bullet_hit_list:
                bullet.kill()
                for asteroid in bullet_hit_list:
                    self.explosion_list.append(sprites.Explosion(asteroid))
                    if asteroid.type == 'coin':
                        self.rocket.coins += 1
                    elif asteroid.type == 'fuel':
                        self.rocket.fuel = self.rocket.max_fuel
                    elif asteroid.type == 'time':
                        pass
                    asteroid.kill()

        self.edge_marker.update()

        self.populate_asteroids()

        arcade.set_viewport(self.rocket.center_x-SCREEN_WIDTH/2, self.rocket.center_x+SCREEN_WIDTH/2,
                            self.rocket.center_y-SCREEN_HEIGHT/2, self.rocket.center_y+SCREEN_HEIGHT/2)

        self.fuel_progress_bar.update(self.rocket.center_x, self.rocket.center_y, self.rocket.fuel/self.rocket.max_fuel)
        self.oxygen_progress_bar.update(self.rocket.center_x, self.rocket.center_y, self.rocket.oxygen/self.rocket.max_oxygen)

        self.background.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.rocket.thrusting = True
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rocket.damping = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.rocket.shoot()
        if key == arcade.key.ESCAPE:
            window.show_view(MenuView())

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.rocket.thrusting = False
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rocket.damping = False

    def on_show_view(self):
        arcade.set_viewport(self.rocket.center_x-SCREEN_WIDTH/2, self.rocket.center_x+SCREEN_WIDTH/2,
                            self.rocket.center_y-SCREEN_HEIGHT/2, self.rocket.center_y+SCREEN_HEIGHT/2)

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
            num = random.random()
            if num <= 0.95:
                type = 'brown' #95% chance of default asteroid
            elif num <= 0.97:
                type = 'coin'  # 2%
            elif num <= 0.99:
                type = 'fuel'  # 2%
            else:
                type = 'time' # 1%
            self.asteroid_list.append(sprites.Asteroid(center_x, center_y, type = type))

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
                for i in range (0, number_of_coins):
                    coin_x = random.randint(chunk[0] * 1000, chunk[0] * 1000 + 1000)
                    coin_y = random.randint(chunk[1] * 1000, chunk[1] * 1000 + 1000)
                    self.coin_list.append(sprites.Coin(coin_x, coin_y, 0.05))




    def on_mouse_motion(self, x, y, dx, dy):
        global MOUSE_X, MOUSE_Y
        MOUSE_X = x
        MOUSE_Y = y

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

    def on_draw(self):
        arcade.start_render()
        self.logo.draw()
        

    def on_show_view(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()


    def setup(self):
        self.ui_manager.purge_ui_elements()

        y_slot = SCREEN_HEIGHT // 4
        x_slot = SCREEN_WIDTH // 4

        self.logo = arcade.Sprite('sprites/menu/logo.png', 1, center_x = x_slot * 2, center_y = y_slot * 3)

        button = buttons.ChangeViewButton(
            'Play',
            x_slot,
            y_slot,
            game_view,
            width = 250
        )

        self.ui_manager.add_ui_element(button)

        button = buttons.FullScreenButton(
            'Toggle Fullscreen',
            x_slot *2,
            y_slot,
            width = 250
        )

        self.ui_manager.add_ui_element(button)
        


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)


    def on_resize(self, width, height):
        global current_screen_width, current_screen_height
        current_screen_width, current_screen_height = self.get_size()


if __name__ == '__main__':
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'Asteroids++')
    game_view = GameView()
    game_view.setup()
    window.show_view(MenuView())
    arcade.run()
