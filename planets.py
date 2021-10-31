import sprites
import buttons


class Earth(sprites.Planet):
    '''Class for earth, child of sprites.Planet class'''

    def __init__(self, rocket, center_x, center_y):
        super().__init__('earth', rocket, 'sprites/planets/earth.png', 1)
        self.center_x = center_x
        self.center_y = center_y
        self.show_edge_marker = 1  # Edge marker shows by default without being upgraded
        # Upgrade button for thrusters, cost multiplies by 2 each time and
        # thrusters amount increases by 1
        self.button_list.append(
            buttons.UpgradeButton(
                'Thrusters',
                'thrusters',
                rocket,
                1,
                cost_multiplier=2,
                upgrade_step=100))
        self.button_list.append(
            buttons.UpgradeButton(
                'Dampers',
                'dampers',
                rocket,
                1,
                cost_multiplier=2,
                upgrade_step=0.5))  # Dampers upgrade button, same values as thrusters
        # Fire rate upgrade, cost multiplies by 2 and upgrade multiplies by 0.9
        # (Time so decrease = better)
        self.button_list.append(
            buttons.UpgradeButton(
                'Fire Rate',
                'shoot_speed',
                rocket,
                1,
                cost_multiplier=2,
                upgrade_multiplier=0.9))
        self.button_list.append(
            buttons.UpgradeButton(
                'Fuel',
                'max_fuel',
                rocket,
                5,
                cost_multiplier=1.5,
                upgrade_step=5))  # Increase max fuel by 5 seconds, cost multiplies by 1.5x
        self.button_list.append(
            buttons.UpgradeButton(
                'Oxygen',
                'max_oxygen',
                rocket,
                5,
                cost_multiplier=1.5,
                upgrade_step=5))  # Same values as fuel
        self.button_list.append(
            buttons.UpgradeButton(
                'Shot Distance',
                'bullet_max_age',
                rocket,
                1,
                cost_multiplier=2,
                upgrade_multiplier=1.5))  # Increases shot distance by increasing maximum age of bullets by 1 second, cost multiplies by 2


class Mars(sprites.Planet):
    def __init__(self, rocket, center_x, center_y):
        super().__init__('mars', rocket, 'sprites/planets/mars.png', 0.6)
        self.center_x = center_x
        self.center_y = center_y
        self.show_edge_marker = 0  # Edge marker hidden by default, needs upgrade to be visible
        self.coins = 0  # Has coins so that upgrades can be applied to attributes using upgrade function

    # mode can be step or multiply depending on how we want to increase the
    # attribute
    def upgrade(self, attribute, step=0, multiply=1):
        '''Upgrade function for mars, allows the planet marker to be made visible through an UpgradeButton'''
        # adds the step value to the attribute (if the step value is at default
        # value of 0 there will be no change)
        setattr(self, attribute, getattr(self, attribute) + step)
        # multiplys the multiply value by the attribute (if the multiply value
        # is at default of 1 there will be no change)
        setattr(self, attribute, getattr(self, attribute) * multiply)
