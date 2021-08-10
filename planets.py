import sprites
import buttons

class Earth(sprites.Planet):
    def __init__(self, rocket, center_x, center_y):

        super().__init__('earth', rocket, 'sprites/planets/earth.png', 1)
        self.button_list.append(buttons.UpgradeButton('Thrusters', 'thrusters', rocket, 1, cost_multiplier = 2, upgrade_step = 100))
        self.button_list.append(buttons.UpgradeButton('Dampers', 'dampers', rocket, 1, cost_multiplier = 2, upgrade_step = 0.5))
        self.button_list.append(buttons.UpgradeButton('Fire Rate', 'shoot_speed', rocket, 1, cost_multiplier = 2, upgrade_multiplier=0.9))
        self.button_list.append(buttons.UpgradeButton('Fuel', 'max_fuel', rocket, 5, cost_multiplier = 1.5, upgrade_step = 5))
        self.button_list.append(buttons.UpgradeButton('Oxygen', 'max_oxygen', rocket, 5, cost_multiplier = 1.5, upgrade_step = 5))
        self.button_list.append(buttons.UpgradeButton('Shot Distance', 'bullet_max_age', rocket, 1, cost_multiplier = 2, upgrade_multiplier= 1.5))


