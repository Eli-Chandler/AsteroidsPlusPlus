import arcade
import math
import random
import buttons


class Rocket(arcade.Sprite):
    '''Class for rocket object - the object that the player controls in the game'''
    def __init__(self, image):
        super().__init__(image, 0.25)

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
        self.max_oxygen = 45
        self.oxygen = 45

        self.velocity_radians = 0

        self.coins = 0

        self.last_shot = 3
        self.shoot_speed = 2

        self.bullet_max_age = 2

        self.bullet_list = arcade.SpriteList()

        self.lives = 3

        self.death_sound = arcade.Sound('sounds/loss.mp3', streaming=True)
        self.shoot_sound = arcade.Sound('sounds/shoot.mp3', streaming=True)

        self.show_edge_marker_mars = False

    def update(self, delta_time, mouse_x, mouse_y):
        '''Called every update of the game, used to check rocket oxygen, value, process movement'''

        if self.oxygen >= self.max_oxygen:
            self.oxygen = self.max_oxygen

        self.oxygen -= delta_time

        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        if self.last_shot >= self.shoot_speed:
            self.last_shot = self.shoot_speed
        else:
            self.last_shot += 1 * delta_time

        if self.at_base:
            self.fuel = self.max_fuel
            self.oxygen = self.max_oxygen

        if self.oxygen < 0:
            self.die()

        mouse_x_relative = mouse_x - current_screen_width / 2
        mouse_y_relative = mouse_y - current_screen_height / 2
        self.radians = math.atan2(mouse_y_relative, mouse_x_relative) - 1.5708 # Sets direction of sprite to point towards mouse from center of the screen

        self.velocity_radians = math.atan2(self.delta_y, self.delta_x) - 1.5708 # Finds direction of rocket in radians
        if self.damping: # If right click is held the rocket will slow down through dampers, dampers are not mouse position dependent
            if self.delta_x > 0:

                change = self.delta_x * \
                    math.sin(self.velocity_radians) * delta_time * self.dampers
                if abs(change) > abs(self.delta_x):
                    self.delta_x = 0
                else:
                    self.delta_x += change

            else:
                change = self.delta_x * \
                    math.sin(self.velocity_radians) * delta_time * self.dampers
                if abs(change) > abs(self.delta_x):
                    self.delta_x = 0
                else:
                    self.delta_x -= change
            if self.delta_y > 0:
                change = self.delta_y * \
                    math.cos(self.velocity_radians) * delta_time * self.dampers
                if abs(change) > abs(self.delta_y):
                    self.delta_y = 0
                else:
                    self.delta_y -= change
            else:
                change = self.delta_y * \
                    math.cos(self.velocity_radians) * delta_time * self.dampers
                if abs(change) > abs(self.delta_y):
                    self.delta_y = 0
                else:
                    self.delta_y += change
        elif self.thrusting and self.fuel > 0:
            self.fuel -= 1 * delta_time
            self.delta_x += -self.thrusters * \
                math.sin(self.radians) * delta_time
            self.delta_y += self.thrusters * \
                math.cos(self.radians) * delta_time

        self.center_x += self.delta_x * delta_time
        self.center_y += self.delta_y * delta_time

    def die(self):
        '''Called when the rocket collides with an asteroid, resets the position and coins of the rocket and removes 1 life
        also plays the rockets death sound'''
        self.center_x = 0
        self.center_y = 0

        self.delta_x = 0
        self.delta_y = 0

        self.coins = 0

        self.lives -= 1

        arcade.play_sound(self.death_sound)

    def shoot(self):
        '''function to make the rocket shoot, the function first checks if the time since the last shot is greater than the shoot speed,
        than creates a new bullet object and adds it to the rockets bullet list'''
        if self.last_shot < self.shoot_speed:
            return

        arcade.play_sound(self.shoot_sound)

        self.delta_x -= -self.recoil * math.sin(self.radians)
        self.delta_y -= self.recoil * math.cos(self.radians)

        delta_x = self.delta_x - 100 * math.sin(self.radians)
        delta_y = self.delta_y + 100 * math.cos(self.radians)
        self.bullet_list.append(
            Bullet(
                self.center_x,
                self.center_y,
                delta_x,
                delta_y,
                self.angle,
                self.bullet_max_age))
        self.last_shot = 0

    # mode can be step or multiply depending on how we want to increase the
    # attribute
    def upgrade(self, attribute, step=0, multiply=1):
        '''Function used to upgrade attributes of the rocket, called by upgrade buttons on planets'''
        setattr(
            self,
            attribute,
            getattr(
                self,
                attribute) +
            step)  # adds the step value to the attribute (if the step value is at default value of 0 there will be no change)
        # multiplys the multiply value by the attribute (if the multiply value
        # is at default of 1 there will be no change)
        setattr(self, attribute, getattr(self, attribute) * multiply)


class Marker(arcade.Sprite):
    '''Sprite that points towards its target at all times, centered around the rocket'''
    def __init__(self, origin, target):
        scale = 1
        image = f'sprites/planets/edge marker_{target.name}.png'
        super().__init__(image, scale)

        self.center_x = origin.center_x
        self.center_y = origin.center_y

        self.origin = origin
        self.target = target

    def update(self):
        '''Updates postion of marker'''
        self.center_x = self.origin.center_x
        self.center_y = self.origin.center_y

        relative_x = self.center_x - self.target.center_x
        relative_y = self.center_y - self.target.center_y

        self.radians = math.atan2(relative_y, relative_x) - 1.5708

    def check_visibility(self, screen_width, screen_height):
        '''Function to check if marker needs to be visible, i.e if planet of marker is on screen it won't be drawn'''

        screen_width = 1280
        screen_height = 720

        if self.center_x + screen_width / 2 > self.target.center_x and self.center_x - \
                screen_width / 2 < self.target.center_x:
            if self.center_y + screen_height / 2 > self.target.center_y and self.center_y - \
                    screen_height / 2 < self.target.center_y:
                return False
        return True


class Bullet(arcade.Sprite):
    '''Class to create rockets bullets, they will explode on contact with asteroids or after a certain amount of time'''
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
        '''Updates position and age of the bullet'''
        self.center_x += self.delta_x * delta_time
        self.center_y += self.delta_y * delta_time

        self.age += 1 * delta_time


ASTEROID_MIN_SIZE = 0.1
ASTEROID_MAX_SIZE = 0.4
ASTEROID_MAX_VELOCITY = 0.1
ASTEROID_MAX_ROTATION_SPEED = 1


class Asteroid(arcade.Sprite):
    '''Class to create randomly generated asteroid at a certain position and of a ceratin type'''
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

        self.explosion_sound = arcade.Sound(
            'sounds/explosion.mp3', streaming=True)
        self.pickup_sound = arcade.Sound('sounds/pickup.mp3', streaming=True)
        self.increase_sound = arcade.Sound(
            'sounds/increase.mp3', streaming=True)

    def update(self):
        '''Updates position and rotation of asteroid'''
        self.angle += self.rotation_speed
        self.center_x += self.delta_x
        self.center_y += self.delta_y

    def shot(self):
        '''Function called when asteroid is shot, currently unused but could be useful if we want certain events to happen when an asteroid is shot'''
        if self.type == 'brown':
            pass
            # delete asteroid
        elif self.type == 'coin':
            pass
            # drop coins
        elif self.type == 'fuel':
            pass
            # drop fuel


EXPLOSION_MAX_AGE = 0.5  # Constant defining max age of explosions in seconds


class Explosion(arcade.Sprite):
    '''Class to create explosion sprite, animation will play at different speed depending on EXPLOSION_MAX_AGE (Default value = 0.5)'''
    def __init__(self, obj, EXPLOSION_MAX_AGE=EXPLOSION_MAX_AGE):
        scale = obj.scale * 1.7
        image = 'sprites/explosion/explosion1_new.png'
        super().__init__(image, scale)

        self.center_x = obj.center_x
        self.center_y = obj.center_y
        self.angle = random.randint(0, 360)
        try:
            self.delta_x = obj.delta_x
        except BaseException:
            pass
        try:
            self.delta_y = obj.delta_y
        except BaseException:
            pass

        self.angle = obj.angle

        self.current_texture = 0

        self.texture_list = [
            'explosion0_new.png',
            'explosion2_new.png',
            'explosion3_new.png',
            'explosion4_new.png',
            'explosion5_new.png',
            'explosion6_new.png',
        ]

        self.texture = arcade.sprite.load_texture(
            f'sprites/explosion/{self.texture_list[0]}')

        self.age = 0
        self.max_age = EXPLOSION_MAX_AGE

        self.anim_frame_time = self.max_age / len(self.texture_list)
        self.current_frame_time = self.anim_frame_time

    def update(self, delta_time):
        '''Update function for Explosion, checks if current age is greater than max age and removes self if so'''
        self.center_x += self.delta_x * delta_time
        self.center_y += self.delta_y * delta_time

        self.age += 1 * delta_time

        if self.age >= self.current_frame_time:
            try:
                self.texture = arcade.sprite.load_texture(
                    f'sprites/explosion/{self.texture_list[self.current_texture]}')
            except BaseException:
                self.kill()
            self.current_texture += 1
            self.current_frame_time += self.anim_frame_time


class Coin(arcade.Sprite):
    '''Class for sprites of coins, used to draw coins on the screen'''
    def __init__(self, center_x, center_y, scale):
        image = 'sprites/coin/coin.png'
        super().__init__(image, scale)

        self.center_x = center_x
        self.center_y = center_y


class ProgressBar(arcade.Sprite):
    '''Bar drawn at the bottom of the screen to represent how close a certain value is to 100% of its maximum value'''
    def __init__(self, height, color):
        scale = 1
        image = f'sprites/bars/{color}.png'
        super().__init__(image, scale)

        self.scale = scale
        self.y_height = height

    def update(self, center_x, center_y, percentage):
        '''Positions bar to be current value/max'''
        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        self.center_x = center_x - 1280 + (self.scale * 1280 * percentage)
        self.center_y = center_y - 720 / 2 + self.y_height


class Background(arcade.Sprite):
    '''Background object, makes the star background move slightly offset to the movement of the rocket'''
    def __init__(self, parent):
        scale = 1
        image = f'sprites/backgrounds/space background.png'
        super().__init__(image, scale)

        self.parent = parent

    def update(self):
        '''Updates positon of background relative of that to the rocket (difference/20)'''
        self.center_x = self.parent.center_x - self.parent.center_x / 20
        self.center_y = self.parent.center_y - self.parent.center_y / 20


class Counter(arcade.Sprite):
    '''Class to show a thumbnail sprite and its current value i.e number of coins or lives'''
    def __init__(self, parent, count, offset_x, offset_y, image, scale=1):
        super().__init__(image, scale)

        self.parent = parent
        self.count = count
        self.offset_x = offset_x
        self.offset_y = offset_y

    def update(self):
        '''Updates positon of counter to always be at a specific offset to the rocket'''
        self.center_x = self.parent.center_x + self.offset_x
        self.center_y = self.parent.center_y + self.offset_y

    def draw(self):
        '''Draws the counter sprite and value onto the screen'''
        if self._sprite_list is None:
            self._sprite_list = arcade.SpriteList()
            self._sprite_list.append(self)

        count = getattr(self.parent, self.count)

        self._sprite_list.draw()
        arcade.draw_text(str(count),
                         self.center_x + 32 * len(str(count)),
                         self.center_y - self.height / 4,
                         arcade.color.WHITE,
                         32)


class Planet(arcade.Sprite):
    '''Planet sprite class button list can be specified to add upgrade buttons on the specific planet'''
    def __init__(self, name, rocket, image, scale):
        super().__init__(image, scale)
        self.name = name
        self.button_list = []
        self.rocket = rocket

    def on_collision(self):
        pass
