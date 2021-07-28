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
    def __init__(self, text, upgrade, subject, cost, cost_multiplier = 1, upgrade_step = 0, upgrade_multiplier = 1):
        
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
        current_screen_width = arcade.get_window().width
        current_screen_height = arcade.get_window().height

        x = x - current_screen_width/2 + rocket_x
        y = y - current_screen_height/2 + rocket_y



        if x <= self.center_x + 50 and x >= self.center_x-50 and y <= self.center_y + 10 and y >= self.center_y - 10 and at_base:
            self.mouse_over = True
        else:
            self.mouse_over = False



    def on_click(self, coin_count):
        if coin_count >= self.cost and self.mouse_over:
            self.subject.upgrade(self.upgrade, self.upgrade_step, self.upgrade_multiplier)


    def draw(self, at_base):
        if at_base:
            if self.mouse_over:
                arcade.draw_rectangle_filled(self.center_x, self.center_y, 110, 30, arcade.color.WHITE)
            arcade.draw_rectangle_filled(self.center_x, self.center_y, 100, 20, arcade.color.GRAY)
            arcade.draw_text(self.text, self.center_x-25, self.center_y-5, arcade.color.BLACK)


