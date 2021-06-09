import arcade
import arcade.gui
from arcade.gui import UIManager

class StartButton(arcade.gui.UIFlatButton):
    def on_click(self):
        print('self')

        #window.show_view(GameView())