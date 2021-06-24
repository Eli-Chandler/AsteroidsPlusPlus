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