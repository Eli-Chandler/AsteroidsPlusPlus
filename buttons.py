import arcade.gui
from arcade.gui import UIManager

class ChangeViewButton(arcade.gui.UIFlatButton):
    def __init__(self, text, center_x, center_y, view, width = 100, height = 100):
        super().__init__(text, center_x, center_y, width, height)

        self.view = view
        self.window = arcade.get_window()

    def on_click(self):

        self.window.show_view(self.view)

class FullScreenButton(arcade.gui.UIFlatButton):
    def __init__(self, text, center_x, center_y, width = 100, height = 100):
        super().__init__(text, center_x, center_y, width, height)

        self.window = arcade.get_window()

    def on_click(self):

        self.window.set_fullscreen(not self.window.fullscreen)


class UpgradeButton():
    def __init__(self, text, upgrade, cost, cost_multiplier = 1.1, upgrade_step = False, upgrade_multiplier = False):
        
        self.center_x = 0
        self.center_y = 0

        self.text = text
        self.upgrade = upgrade

        self.cost = cost
        self.multiplier = cost_multiplier
        self.upgrade_step = upgrade_step
        self.upgrade_multiplier = upgrade_multiplier

    def check_click(self, x, y, at_base):
        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        x = x - current_screen_width/2
        y = y - current_screen_height/2

        if x <= self.center_x + 50 and x >= self.center_x-50 and y <= self.center_y + 10 and y >= self.center_y - 10:
            return True
        return False



    def on_click(self, coin_count):
        if coin_count >= self.cost:
            coin_count -= self.cost
            self.cost *= cost_multiplier
            if self.upgrade_step:
                self.upgrade += self.upgrade_step
            else:
                self.upgrade *= self.upgrade_multiplier


    def draw(self, at_base):
        if at_base:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, 100, 20, arcade.color.GRAY)
            arcade.draw_text(self.text, self.center_x-25, self.center_y-5, arcade.color.BLACK)
