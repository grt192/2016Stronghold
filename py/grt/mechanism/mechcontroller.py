class MechController:
    def __init__(self, driver_joystick, xbox_controller, shooter, belt_roller_motor):  # mechanisms belong in arguments
        # define mechanisms here
        self.shooter = shooter

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        self.belt_roller_motor = belt_roller_motor
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)

    def _xbox_controller_listener(self, sensor, state_id, datum):

        if state_id == "x_button":
            if datum:
                self.shooter.flywheel.increment_speed()
        if state_id == "y_button":
            if datum:
                self.shooter.flywheel.decrement_speed()
        if state_id == "b_button":
            if datum:
                self.belt_roller_motor.set(.8)
            else:
                self.belt_roller_motor.set(0)
        if state_id == "a_button":
            if datum:
                self.shooter.flywheel.spin_to_standby_speed()

    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == "button4":
            if datum:
                self.shooter.start_automatic_shot()
        if state_id == "button5":
            if datum:
                self.shooter.abort_automatic_shot()
        if state_id == "button6":
            if datum:
                self.shooter.flywheel_motor.set(0)
