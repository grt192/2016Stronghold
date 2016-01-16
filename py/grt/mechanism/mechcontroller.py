class MechController:

    def __init__(self, driver_joystick, xbox_controller, vision_mech): # mechanisms belong in arguments
        # define mechanisms here
        self.vision_mech = vision_mech

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)

    def _xbox_controller_listener(self, sensor, state_id, datum):
        pass

    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == "button4":
            if datum:
                self.vision_mech.vision_enabled = True
        if state_id == "button5":
            self.vision_mech.vision_enabled = False