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

class UpgradeButton(arcade.gui.UIFlatButton):
    def __init__(self, text, parent, upgrade, cost, cost_multiplier = 1.1, upgrade_step = False, upgrade_multiplier = False):
        super().__init__(text)
        self.parent = parent
        self.upgrade = upgrade
        self.cost = cost
        self.multiplier = cost_multiplier
        self.upgrade_step = upgrade_step
        self.upgrade_multiplier = upgrade_multiplier
    def on_click(self, coin_count):
        if coin_count >= self.cost:
            coin_count -= self.cost
            self.cost *= cost_multiplier
            if self.upgrade_step:
                self.upgrade += self.upgrade_step
            else:
                self.upgrade *= self.upgrade_multiplier

        print('test')
