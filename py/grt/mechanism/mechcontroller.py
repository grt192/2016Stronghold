class MechController:

    def __init__(self, driver_joystick, xbox_controller, shooter,flywheel): # mechanisms belong in arguments
        # define mechanisms here
        self.shooter = shooter

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        self.flywheel = flywheel
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)


    def _xbox_controller_listener(self, sensor, state_id, datum):
        if state_id == "x_button":
            if datum:
                self.flywheel.speed_increment_function()
        if state_id == "y_button":
            if datum:
                self.flywheel.speed_decrement_function()



    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == "button4":
            if datum:
                self.shooter.start_automatic_shot()
        if state_id == "button5":
            if datum:
                self.shooter.abort_automatic_shot()