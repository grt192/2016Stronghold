class MechController:

    def __init__(self, driver_joystick, xbox_controller, flywheel): # mechanisms belong in arguments
        # define mechanisms here
        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        self.flywheel = flywheel
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)

    def _xbox_controller_listener(self, sensor, state_id, datum):
        if state_id == "y_button":
            if datum:
                self.flywheel.increment()

        if state_id == "x_button":
            if datum:
                self.flywheel.decrement()

    def _driver_joystick_listener(self, sensor, state_id, datum):
        pass