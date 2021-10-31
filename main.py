'''
Credits:
Sound effects made with Leshy FXMaker https://www.leshylabs.com/apps/sfMaker/
Explosion Animation Sprite made by PNGWing https://w7.pngwing.com/pngs/879/232/png-transparent-sprite-gamemaker-studio-animation-2d-computer-graphics-explosion-sprite-text-orange-2d-computer-graphics.png
'''

import logging
import arcade
import arcade.gui
from arcade.gui import UIManager

import random
import math
from datetime import datetime

import sprites
import buttons
import planets

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
current_screen_height = SCREEN_HEIGHT
current_screen_width = SCREEN_WIDTH

MOUSE_X = 0
MOUSE_Y = 0

USE_SPATIAL_HASHING = False

won = False


class GameView(arcade.View):
    def __init__(self):
        '''Initializes all variables for the game'''
        super().__init__()

        self.rocket = None
        self.rocket_list = None
        self.dead = None

        self.asteroid_list = None
        self.explosion_list = None

        self.coin_list = None
        self.existing_chunks = None
        self.BASE_ASTEROID_COUNT = None

        self.score = None

        self.ui_manager = UIManager()
        self.edge_marker_list = None
        self.fuel_progress_bar = None
        self.oxygen_progress_bar = None
        self.shoot_progress_bar = None
        self.coin_counter = None
        self.lives_counter = None

        self.background = None

        self.music = None
        self.music_player = None
        self.music_enabled = True

        self.planet_list = None

    def setup(self):
        '''Can be called to reset the game back to its original states - resets all variables to default value'''

        self.music = arcade.Sound('music.mp3', streaming=True) # Adds music.mp3 as a sound in the game
        self.music_player = self.music.play() # Starts music

        self.fuel_progress_bar = sprites.ProgressBar(5, 'green')

        self.oxygen_progress_bar = sprites.ProgressBar(15, 'blue')

        self.shoot_progress_bar = sprites.ProgressBar(25, 'red')

        arcade.set_background_color(arcade.color.BLACK)

        self.explosion_list = arcade.SpriteList() # Creates a spritelist for explosions

        self.score = 0

        self.BASE_ASTEROID_COUNT = 100 # Defines how many asteroids are on screen at once

        self.existing_chunks = [] # Defines chunks that have already been generated for coins

        self.MAX_COINS = 1 # Base number of coins per chunk, increases with distance from earth
        self.coin_list = arcade.SpriteList() # Creates spritelist for coins

        self.rocket_list = arcade.SpriteList() # Creates spritelist
        self.rocket = sprites.Rocket('sprites/rocket/still.png') # Creates rocket object
        self.rocket_list.append(self.rocket) # Appends rocket to rocket list

        self.asteroid_list = arcade.SpriteList(
            use_spatial_hash=USE_SPATIAL_HASHING) # Creates asteroid list and disables spatial hashing - IMPORTANT for performance

        self.planet_list = arcade.SpriteList()

        self.earth = planets.Earth(self.rocket, 0, 0)

        x = [random.randint(4000, 5000), random.randint(-5000, -4000)]
        y = [random.randint(4000, 5000), random.randint(-5000, -4000)] # Creates random position for mars 
        self.mars = planets.Mars(
            self.rocket,
            random.choice(x),
            random.choice(y)) # Creates mars object in random position

        self.earth.button_list.append(
            buttons.UpgradeButton(
                'Mars location',
                'show_edge_marker_mars',
                self.rocket,
                30,
                cost_multiplier=0,
                upgrade_step=1)) # Adds mars location button to earth button list - cost multiplier 0 makes it so it can only be purchased once

        self.planet_list.append(self.earth)
        self.planet_list.append(self.mars) #Adds earth and mars to planet list
        # self.planet_list.append(self.mars)

        self.edge_marker_list = arcade.SpriteList() # Creates list for plant edge markers

        for planet in self.planet_list: # Adds a marker for each planet in the game
            edge_marker = sprites.Marker(self.rocket, planet)
            self.edge_marker_list.append(edge_marker) # Creates and adds planet edge markers to edge marker list

        self.background = sprites.Background(self.rocket) # Creates background that moves relative to rocket

        self.position_buttons() # Generate positions for each button in planets button lists

        self.coin_counter = sprites.Counter(
            self.rocket,
            'coins',
            -current_screen_width / 2 + 50,
            current_screen_height / 2 - 50,
            'sprites/coin/gold.png',
            1.5) # Creates a counter for coins

        self.lives_counter = sprites.Counter(
            self.rocket,
            'lives',
            -current_screen_width / 2 + 50,
            current_screen_height / 2 - 100,
            'sprites/rocket/still.png',
            0.25) # Creates a counter for lives

        self.populate_spawn_asteroids() # Populates initial asteroids so screen is not empty

        self.frame_rate_list = [] # Used to calculate average FPS

        self.rocket.lives = 3 # Defines number of times rocket can die

    def play_music(self):
        '''If music is not currently playing the function will start music, called in update() function'''
        if not self.music.is_playing(self.music_player):
            self.music = arcade.Sound('music.mp3', streaming=True)
            self.music_player = self.music.play() # If music is no longer playing it will play it again

    def on_draw(self):
        # Parent function, called every frame of the game used to draw elements onto the screen

        arcade.start_render()

        self.background.draw() # Draws background

        self.planet_list.draw() # Draws every planet in planet list

        self.coin_list.draw() # Draws every coin in coin list

        if self.edge_marker_list[0].check_visibility(
                current_screen_width, current_screen_height):
            self.edge_marker_list[0].draw() # Checks if earth edge marker should be visible and draws it
        if self.edge_marker_list[1].check_visibility(
                current_screen_width,
                current_screen_height) and self.rocket.show_edge_marker_mars:
            self.edge_marker_list[1].draw() # checks if mars edge marker should be visibile and draws it

        for planet in self.planet_list:
            for button in planet.button_list:
                button.draw(self.rocket.at_base) # Draws every button for each planet (Has to draw each seperately because they use a custom draw function)

        self.rocket.draw() # Draws rocket

        self.asteroid_list.draw() # Draws every asteroid in asteroid list

        self.explosion_list.draw() # Draws every explosion in explosion list

        self.fuel_progress_bar.draw()
        self.oxygen_progress_bar.draw()
        self.shoot_progress_bar.draw() # Draws progress bars, not part of a list so they need to be drawn seperately

        self.coin_counter.draw()
        self.lives_counter.draw() # Draws counters, not part of a list so they need to be drawn seperately

        self.rocket.bullet_list.draw() # Draws rocket bullets

    def on_update(self, delta_time):
        # Parent function, called on every update of the game - used to update positions, velocities etc.

        for planet in self.planet_list:
            planet_hit_list = arcade.check_for_collision_with_list(
                planet, self.asteroid_list) # Checks collisions with asteroids for each planet

            # if planet_hit_list:
            # if planet.name == 'mars':
            # window.show_view(MenuView())

            for asteroid in planet_hit_list:
                self.explosion_list.append(sprites.Explosion(asteroid))
                arcade.play_sound(asteroid.explosion_sound)
                asteroid.kill() # Deletes each asteroid that hits a planet and plays explosion sound and animation

        if self.rocket.lives <= 0:
            self.rocket.lives = 3
            window.show_view(LoseView()) # If rocket is out of lives the game will show the loseview and reset the game

        self.mars.coins = self.rocket.coins # Mars coins are set to the same at rocket coins, this is necessary because of the way upgrades work, and the mars marker being a subject of mars

        if self.music_enabled:
            self.play_music() # Plays music if music is enabled

        self.explosion_list.update_animation() # Plays through all explosions animations

        for explosion in self.explosion_list:
            explosion.update(delta_time) # Adds delta_time to explosions age

        for bullet in self.rocket.bullet_list:
            bullet.update(delta_time)
            if bullet.age >= bullet.max_age:
                self.explosion_list.append(sprites.Explosion(bullet))
                bullet.kill() # Updates bullet with delta_time to increase age, if bullet age is greater than max age it kills it and creates an explosion

        self.coin_list.update() # Updates coin list
        # self.populate_coins()

        self.planet_list.update() # Updates each planet in the planet list

        self.rocket.update(delta_time, MOUSE_X, MOUSE_Y) # Updates rocket with delta time and mouse position to allow for movement, velocity and angle calculations

        self.asteroid_list.update() # Updates each asteroid in asteroid list, updates position and angle

        for planet in self.planet_list:
            self.rocket.at_base = arcade.check_for_collision(
                self.rocket, planet) # Checks if rocket is at a planet

            if self.rocket.at_base and planet.name == 'mars' and not won:
                window.show_view(WinView()) # If the rocket is it mars and it has not already been to mars before the win screen will display (only shows once)

            if self.rocket.at_base:
                break # Only checks if it is at 1 planet since it can't be 2 places at once

        else:
            self.rocket.at_base = False # For else statement - if the for loop is not broken it will set rocket.at_base to false

        coin_hit_list = arcade.check_for_collision_with_list(
            self.rocket, self.coin_list) # Checks if the rocket has collied with any coins and adds those coins to al ist

        for coin in coin_hit_list:
            coin.kill()
            self.rocket.coins += 5 # Coins in coin list are deleted and adds 5 coins to rocket

        for bullet in self.rocket.bullet_list:
            bullet_hit_list = arcade.check_for_collision_with_list(
                bullet, self.asteroid_list) # Checks for collisions between bullets and asteroids and adds it to list
            if bullet_hit_list:
                bullet.kill() # Deletes bullet
                for asteroid in bullet_hit_list:
                    self.explosion_list.append(sprites.Explosion(asteroid))
                    if asteroid.type == 'coin':
                        self.rocket.coins += 5 # If the asteroid is a coin asteroid 5 coins are added to rocket
                        arcade.play_sound(asteroid.pickup_sound)
                    elif asteroid.type == 'fuel':
                        self.rocket.fuel = self.rocket.max_fuel # If the asteroid is a fuel asteroid the rocket gets refueled to max fuel
                        arcade.play_sound(asteroid.increase_sound)
                    elif asteroid.type == 'time':
                        self.rocket.oxygen += 10 # If the asteroid is an oxygen asteroid the rocket gets 10 seconds of fuel
                        arcade.play_sound(asteroid.increase_sound)
                    else:
                        arcade.play_sound(asteroid.explosion_sound) # If it is a normal asteroid it will simply explode
                    asteroid.kill() # Asteroid is deleted

        self.edge_marker_list.update() # Updates all edge markers

        self.populate_asteroids() # Populates asteroid, every time 1 asteroid goes off the screen a new one will be spawned

        arcade.set_viewport(
            self.rocket.center_x - SCREEN_WIDTH / 2,
            self.rocket.center_x + SCREEN_WIDTH / 2,
            self.rocket.center_y - SCREEN_HEIGHT / 2,
            self.rocket.center_y + SCREEN_HEIGHT / 2) # Centers viewport around rocket

        self.fuel_progress_bar.update(
            self.rocket.center_x,
            self.rocket.center_y,
            self.rocket.fuel /
            self.rocket.max_fuel) 
        self.oxygen_progress_bar.update(
            self.rocket.center_x,
            self.rocket.center_y,
            self.rocket.oxygen /
            self.rocket.max_oxygen)
        self.shoot_progress_bar.update(
            self.rocket.center_x,
            self.rocket.center_y,
            self.rocket.last_shot /
            self.rocket.shoot_speed) # Updates fuel progress bar to update position on screen and % full

        self.background.update()
        for planet in self.planet_list:
            for button in planet.button_list:
                button.check_mouse(
                    MOUSE_X,
                    MOUSE_Y,
                    self.rocket.center_x,
                    self.rocket.center_y,
                    self.rocket.at_base) # Checks if a button is moused over so a white background can be added to highlight

        self.coin_counter.update() # Updates coin counter
        self.lives_counter.update() # Updates lives counter

        asteroid_hit_list = arcade.check_for_collision_with_list(
            self.rocket, self.asteroid_list) # Checks for collision between rocket and asteroids and adds to list

        if asteroid_hit_list:
            if not self.rocket.invincible:
                if not self.rocket.at_base:
                    for asteroid in self.asteroid_list:
                        self.asteroid_list.remove(asteroid) # Removes all asteroids
                    self.populate_spawn_asteroids() # Repopulates spawn area with asteroids
                    self.rocket.die() # Kills rocket - subtracts life and returns to earth

    def on_mouse_press(self, x, y, button, modifiers):
        # Parent function, called when a mouse button is pressed
        if button == arcade.MOUSE_BUTTON_LEFT: # If left mouse button is pressed
            button_ = False 
            for planet in self.planet_list:
                for button in planet.button_list:
                    button.on_click()
                    if button.mouse_over:
                        button_ = True # Checks if user is clicking on a button
            if not button_: # If user is clicking on a button the rocket will not thrust
                self.rocket.thrusting = True # Only runs if user is not clicking a button

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rocket.damping = True # If Right mouse button is pressed damping is run - rocket slows down

    def on_key_press(self, key, modifiers):
        # Parent function, called when a keyboard key is pressed
        if key == arcade.key.SPACE:
            self.rocket.shoot()
        if key == arcade.key.ESCAPE:
            window.show_view(MenuView()) # Shows pause menu if escape is pressed

    def on_mouse_release(self, x, y, button, modifiers):
        # Parent function, called when a mouse button is released
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.rocket.thrusting = False
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rocket.damping = False

    def position_buttons(self):
        '''Positions buttons around buttons in self.planet list, but only if the rocket is touching that planet'''
        for planet in self.planet_list:
            length = len(planet.button_list) # Gets number of buttons
            space = 300 # Space between buttons (px)

            n = 0
            for button in planet.button_list:
                if n % 2 == 0: # Puts half the buttons on the right and half on the left, spaced with space pixels in between vertically
                    button.center_x = -100 # If buttons want to be added for other planets this should be changed to planet.center_x - 100!
                    button.center_y = space / length * n - space / 4
                else:
                    button.center_x = 100
                    button.center_y = space / length * (n - 1) - space / 4
                n += 1

    def on_show_view(self):
        # Parent function, called when view is shown
        self.ui_manager.purge_ui_elements()
        arcade.set_viewport(
            self.rocket.center_x - SCREEN_WIDTH / 2,
            self.rocket.center_x + SCREEN_WIDTH / 2,
            self.rocket.center_y - SCREEN_HEIGHT / 2,
            self.rocket.center_y + SCREEN_HEIGHT / 2) # Centers viewport around rocket on startup


    def get_exterior_coords(self):
        '''Function to get coordinates of screen edge, can be used for calculations of what is on screen'''

        # Get coordinates of screen edge
        left = self.rocket.center_x - SCREEN_WIDTH / 2
        right = self.rocket.center_x + SCREEN_WIDTH / 2

        top = self.rocket.center_y + SCREEN_HEIGHT / 2
        bottom = self.rocket.center_y - SCREEN_HEIGHT / 2

        return left, right, top, bottom

    def populate_spawn_asteroids(self):
        '''Function called in setup() to fill the screen with asteroids on spawn, should only be called once'''
        left, right, top, bottom = [int(i) for i in self.get_exterior_coords()] # Maps values for edge of screen co-ordinates

        n = 0
        new = self.asteroid_list # Creates a new asteroid list 
        for asteroid in self.asteroid_list:
            if asteroid.center_x > right + 100 or asteroid.center_x < left - 100:
                new.pop(n) 

            elif asteroid.center_y > top + 100 or asteroid.center_y < bottom - 100:
                new.pop(n) # If asteroid is greater than 100 pixels off screen in any direction it is removed

            n += 1

        self.asteroid_list = new

        amount = self.BASE_ASTEROID_COUNT - len(self.asteroid_list) # Finds how many asteroids were removed

        for i in range(amount):

            center_x = random.randint(-current_screen_width /
                                      2 - 100, current_screen_width / 2 + 100)
            center_y = random.randint(-current_screen_width /
                                      2 - 100, current_screen_height / 2 + 100)

            num = random.random()
            if num <= 0.8:
                type = 'brown'  # 80% chance of default asteroid
            elif num <= 0.9:
                type = 'coin'  # 10%
            elif num <= 0.95:
                type = 'fuel'  # 5%
            else:
                type = 'time'  # 5%
            self.asteroid_list.append(
                sprites.Asteroid(
                    center_x, center_y, type=type)) # Replaces removed asteroids with random odds, places anywhere on screen including the active viewport, should ony be called on startup!

    def populate_asteroids(self):
        '''Function called in update() to fill the screen with asteroids,
        when one asteroid goes off the screen it will be deleted and another will be added'''

        left, right, top, bottom = [int(i) for i in self.get_exterior_coords()]

        n = 0
        new = self.asteroid_list # Creates a new asteroid list 
        for asteroid in self.asteroid_list:
            if asteroid.center_x > right + 100 or asteroid.center_x < left - 100:
                new.pop(n)

            elif asteroid.center_y > top + 100 or asteroid.center_y < bottom - 100:
                new.pop(n) # If asteroid is greater than 100 pixels off screen in any direction it is removed

            n += 1

        self.asteroid_list = new

        amount = self.BASE_ASTEROID_COUNT - len(self.asteroid_list)

        for i in range(amount):

            while True:
                center_x = random.randint(left - 100, right + 100)
                center_y = random.randint(bottom - 100, top + 100)

                if center_x > left - 20 and center_x < right + \
                        20 and center_y > bottom - 20 and center_y < top + 20:
                    continue
                break
            num = random.random()
            if num <= 0.8:
                type = 'brown'  # 80% chance of default asteroid
            elif num <= 0.9:
                type = 'coin'  # 10%
            elif num <= 0.95:
                type = 'fuel'  # 5%
            else:
                type = 'time'  # 5%
            self.asteroid_list.append(
                sprites.Asteroid(
                    center_x, center_y, type=type)) # replaces removed asteroids with new asteroids off screen, so that the asteroid renewal process is seamless

    def populate_coins(self):
        '''Function used to populate coins around the map,
        the farther from the center of the world the more
        coins will spawn'''
        chunk_x = round(self.rocket.center_x / 1000)
        chunk_y = round(self.rocket.center_y / 1000)

        nearby_chunks = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                nearby_chunks.append((chunk_x + i, chunk_y + j))
        for chunk in nearby_chunks:
            if chunk not in self.existing_chunks:
                self.existing_chunks.append(chunk)
                number_of_coins = self.MAX_COINS + \
                    int((chunk[0]**2 + chunk[1]**2)**0.5 / 3)
                number_of_coins = random.randint(1, number_of_coins)
                for i in range(0, number_of_coins):
                    coin_x = random.randint(
                        chunk[0] * 1000, chunk[0] * 1000 + 1000)
                    coin_y = random.randint(
                        chunk[1] * 1000, chunk[1] * 1000 + 1000)
                    self.coin_list.append(sprites.Coin(coin_x, coin_y, 0.05)) # Populates coins in chunks on the screen 

    def on_mouse_motion(self, x, y, dx, dy):
        # Function called when mouse is moved
        global MOUSE_X, MOUSE_Y
        MOUSE_X = x  # Sets global MOUSE_X variable to current mouse x position for use in other calculations
        MOUSE_Y = y


class WinView(arcade.View):
    def __init__(self):
        '''Initializes all variables used in the win view'''
        super().__init__()

        self.ui_manager = UIManager()
        self.background_sprite = None

    def on_draw(self):
        # Parent function, called on each frame of the game, used to draw elements onto the screen
        arcade.start_render()

        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        arcade.set_viewport(0, current_screen_width - 1,
                            0, current_screen_height - 1)  # Resets viewport to default

        # Used to position elemenets in 4 x and y slots on the screen
        y_slot = SCREEN_HEIGHT // 4
        x_slot = SCREEN_WIDTH // 4

        self.background_sprite.draw()
        self.victory_sprite.draw()

        self.background_sprite.center_x = current_screen_width / 2
        self.background_sprite.center_y = current_screen_width / 2 # Centers background sprite

        arcade.draw_text(
            'Thats all the content in the game for now, feel free to continue in free play by pressing this button!',
            x_slot,
            y_slot *
            2,
            arcade.color.GREEN)

    def setup(self):
        '''Setup function, used to reset the winview if it needs to be called again'''
        y_slot = SCREEN_HEIGHT // 4
        x_slot = SCREEN_WIDTH // 4
        self.victory_sprite = arcade.Sprite(
            'sprites/menu/victory.png',
            1,
            center_x=x_slot * 2,
            center_y=y_slot * 3)

        self.background_sprite = arcade.Sprite(
            'sprites/backgrounds/space background.png', 1)
        self.background_sprite.center_x = 1280 / 2
        self.background_sprite.center_y = 720 / 2

        # self.background_sprite = arcade.Sprite('sprites/backgrounds/space background.png', 1, 1280/2, 720/2)

        button = buttons.ChangeViewButton(
            'Play',
            x_slot,
            y_slot,
            game_view,
            width=250
        ) # Adds a change view button that changes the view to game_view

        self.ui_manager.add_ui_element(button)

    def on_hide_view(self):
        # Get rid of buttons when the view is hidden
        self.ui_manager.unregister_handlers()

    def on_show_view(self):
        self.setup()
        global won
        won = True # Sets won value to true so that this view won't show multiple times
        arcade.set_viewport(0, current_screen_width - 1,
                            0, current_screen_height - 1)  # Reset viewport


class LoseView(arcade.View):
    def __init__(self):
        '''Function to initialize all variables used in the lose view'''
        super().__init__()

        self.ui_manager = UIManager()
        self.background_sprite = None

    def on_draw(self):
        # Parent function called on each frame of the game
        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        arcade.set_viewport(0, current_screen_width - 1,
                            0, current_screen_height - 1)  # Reset viewport
        arcade.start_render()

        y_slot = SCREEN_HEIGHT // 4
        x_slot = SCREEN_WIDTH // 4

        self.background_sprite.draw()
        self.lose_sprite.draw()

        self.background_sprite.center_x = x_slot * 2
        self.background_sprite.center_y = y_slot * 2 # Centers background sprite

        arcade.draw_text('You lost!', x_slot, y_slot * 2, arcade.color.RED)

    def setup(self):
        y_slot = SCREEN_HEIGHT // 4
        x_slot = SCREEN_WIDTH // 4
        self.lose_sprite = arcade.Sprite(
            'sprites/menu/failure.png',
            1,
            center_x=x_slot * 2,
            center_y=y_slot * 3)

        self.background_sprite = arcade.Sprite(
            'sprites/backgrounds/space background.png', 1)
        self.background_sprite.center_x = 1280 / 2
        self.background_sprite.center_y = 720 / 2

        # self.background_sprite = arcade.Sprite('sprites/backgrounds/space background.png', 1, 1280/2, 720/2)

        button = buttons.ChangeViewButton(
            'Play Again',
            x_slot,
            y_slot,
            game_view,
            width=250
        ) # Adds changeViewButton to switch back to game view

        self.ui_manager.add_ui_element(button)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_show_view(self):
        self.setup()

        game_view.setup()


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

        self.logo = arcade.Sprite(
            'sprites/menu/logo.png',
            1,
            center_x=x_slot * 2,
            center_y=y_slot * 3)

        button = buttons.ChangeViewButton(
            'Play',
            x_slot,
            y_slot,
            game_view,
            width=250
        ) # adds change view button to change to game view

        self.ui_manager.add_ui_element(button)

        button = buttons.ChangeViewButton(
            'Tutorial',
            x_slot * 3,
            y_slot * 2,
            TutorialView(),
            width=250
        ) # Adds change view button to change to new tutorial view

        self.ui_manager.add_ui_element(button)

        button = buttons.FullScreenButton(
            'Toggle Fullscreen',
            x_slot * 2,
            y_slot,
            width=250
        ) # Adds togle fullscreen button

        self.ui_manager.add_ui_element(button)

        button = buttons.MusicButton(
            game_view,
            x_slot * 3,
            y_slot,
            width=250
        ) # Adds toggle music button

        self.ui_manager.add_ui_element(button)


class TutorialView(arcade.View):
    '''View that includes image that explains how to play the game and a back to menu button'''
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

    def on_draw(self):
        arcade.start_render()

        self.background_sprite.draw()
        self.tutorial.draw() # Draws tutorial sprite

        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        arcade.set_viewport(0, current_screen_width - 1,
                            0, current_screen_height - 1)

        self.tutorial.center_x = current_screen_width / 2
        self.tutorial.center_y = current_screen_height / 2 # Centers tutorial sprite

        self.background_sprite.center_x = current_screen_width / 2
        self.background_sprite.center_y = current_screen_height / 2 # Centers background sprite

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

        self.tutorial = arcade.Sprite(
            'sprites/menu/tutorial.png',
            1,
            center_x=x_slot * 2,
            center_y=y_slot * 2) # Creates new sprite for tutorial
        self.background_sprite = arcade.Sprite(
            'sprites/backgrounds/space background.png', 1)
        self.background_sprite.center_x = 1280 / 2
        self.background_sprite.center_y = 720 / 2

        button = buttons.ChangeViewButton(
            'Back',
            x_slot,
            y_slot,
            MenuView(),
            width=250
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
        # gets new window size and defines globally so elements can be repositioned
        current_screen_width, current_screen_height = self.get_size()


if __name__ == '__main__':
    # Only runs if run directly, not imported
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'Asteroids++')
    game_view = GameView() # Creates new game view
    game_view.setup() # Sets up game view
    window.show_view(MenuView()) # Shows menu view on startup
    arcade.run()
