import sprites
import buttons

class Earth(sprites.Planet):
    def __init__(self, rocket, center_x, center_y):
        super().__init__('earth', rocket, 'sprites/planets/earth.png', 1)
        self.center_x = center_x
        self.center_y = center_y
        self.show_edge_marker = 1
        self.button_list.append(buttons.UpgradeButton('Thrusters', 'thrusters', rocket, 1, cost_multiplier = 2, upgrade_step = 100))
        self.button_list.append(buttons.UpgradeButton('Dampers', 'dampers', rocket, 1, cost_multiplier = 2, upgrade_step = 0.5))
        self.button_list.append(buttons.UpgradeButton('Fire Rate', 'shoot_speed', rocket, 1, cost_multiplier = 2, upgrade_multiplier=0.9))
        self.button_list.append(buttons.UpgradeButton('Fuel', 'max_fuel', rocket, 5, cost_multiplier = 1.5, upgrade_step = 5))
        self.button_list.append(buttons.UpgradeButton('Oxygen', 'max_oxygen', rocket, 5, cost_multiplier = 1.5, upgrade_step = 5))
        self.button_list.append(buttons.UpgradeButton('Shot Distance', 'bullet_max_age', rocket, 1, cost_multiplier = 2, upgrade_multiplier= 1.5))


class Mars(sprites.Planet):
    def __init__(self, rocket, center_x, center_y):
        super().__init__('mars', rocket, 'sprites/planets/mars.png', 0.6)
        self.center_x = center_x
        self.center_y = center_y
        self.show_edge_marker = 0
        self.coins = 0

    def upgrade(self, attribute, step = 0, multiply = 1 ): #mode can be step or multiply depending on how we want to increase the attribute
        setattr(self, attribute, getattr(self, attribute) + step) #adds the step value to the attribute (if the step value is at default value of 0 there will be no change)
        setattr(self, attribute, getattr(self, attribute) * multiply) #multiplys the multiply value by the attribute (if the multiply value is at default of 1 there will be no change)
    
        

