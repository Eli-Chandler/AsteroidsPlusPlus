import arcade.gui
from arcade.gui import UIManager


class ChangeViewButton(arcade.gui.UIFlatButton):
    '''Button used to switch to another specified view'''

    def __init__(self, text, center_x, center_y, view, width=100, height=100):
        super().__init__(text, center_x, center_y, width, height)

        self.view = view
        self.window = arcade.get_window()

    def on_click(self):

        self.window.show_view(self.view)


class MusicButton(arcade.gui.UIFlatButton):
    '''Button used to toggle music on and off'''

    def __init__(self, view, center_x, center_y, width=100, height=100):

        text = 'Toggle Music'
        super().__init__(text, center_x, center_y, width, height)
        self.view = view

    def on_click(self):

        self.view.music_enabled = not self.view.music_enabled


class FullScreenButton(arcade.gui.UIFlatButton):
    '''Button used to toggle fullscreen on and off'''

    def __init__(self, text, center_x, center_y, width=100, height=100):
        super().__init__(text, center_x, center_y, width, height)

        self.window = arcade.get_window()

    def on_click(self):

        self.window.set_fullscreen(not self.window.fullscreen)


class ToggleAttributeButton(arcade.gui.UIFlatButton):
    '''Used to toggle the value of a specific attribute in a view from true to false or false to true'''

    def __init__(
            self,
            text,
            center_x,
            center_y,
            view,
            attribute,
            width=100,
            height=100):
        super().__init__(text, center_x, center_y, width, height)

        self.view = view
        self.attribute = attribute

    def on_click(self):
        setattr(
            self.view,
            self.attribute,
            not getattr(
                self.view,
                self.attribute))


class UpgradeButton():
    '''Custom button class used to upgrade a specific attribute of the subject, increase in cost of the upgrade can either
    be increased by a fixed step with upgrade_step or a multiplier with upgrade_multiplier (leave as default value if one is unused).
    Upgrade buttons should go inside a planet button list'''

    def __init__(
            self,
            text,
            upgrade,
            subject,
            cost,
            cost_multiplier=1,
            upgrade_step=0,
            upgrade_multiplier=1):

        self.center_x = 0
        self.center_y = 0

        self.text = text

        self.upgrade = upgrade
        self.subject = subject

        self.cost = cost
        self.cost_multiplier = cost_multiplier

        self.upgrade_step = upgrade_step
        self.upgrade_multiplier = upgrade_multiplier

        self.mouse_over = True

    def check_mouse(self, x, y, rocket_x, rocket_y, at_base):
        '''Function to check if the mouse is positioned over the button'''
        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        x = x - current_screen_width / 2 + rocket_x
        y = y - current_screen_height / 2 + rocket_y

        x = x / current_screen_width * 1280
        y = y / current_screen_height * 720

        if x <= self.center_x + 50 and x >= self.center_x - \
                50 and y <= self.center_y + 15 and y >= self.center_y - 15 and at_base:
            self.mouse_over = True
        else:
            self.mouse_over = False

    def on_click(self):
        '''Called when a button is clicked, checks if the player has enough coins and calls the subjects upgrade function if so'''
        if self.subject.coins >= self.cost and self.mouse_over:
            self.subject.upgrade(
                self.upgrade,
                self.upgrade_step,
                self.upgrade_multiplier)
            self.subject.coins -= self.cost
            self.cost *= self.cost_multiplier
            self.cost = int(self.cost)

    def draw(self, at_base):
        '''Draw the button, if mouse is positioned over it a white outline will appear'''
        if at_base:
            if self.mouse_over:
                arcade.draw_rectangle_filled(
                    self.center_x, self.center_y, 110, 40, arcade.color.WHITE)
            arcade.draw_rectangle_filled(
                self.center_x, self.center_y, 100, 30, arcade.color.GRAY)
            arcade.draw_text(
                self.text + f'\n({self.cost} Coins)',
                self.center_x - 35,
                self.center_y - 15,
                arcade.color.BLACK)
