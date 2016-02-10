class MechController:

    def __init__(self, driver_joystick, xbox_controller, pickup, manual_shooter): # mechanisms belong in arguments
        # define mechanisms here
        

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        
        self.pickup = pickup
        self.manual_shooter = manual_shooter
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)


    def _xbox_controller_listener(self, sensor, state_id, datum):
        """
        if state_id == "x_button":
            if datum:
                self.shooter.flywheel.speed_increment_function()
        if state_id == "y_button":
            if datum:
                self.shooter.flywheel.speed_decrement_function()
        if state_id == "b_button":
            if datum:
                self.belt_roller_motor.set(.8)
            else:
                self.belt_roller_motor.set(0)
        if state_id == "a_button":
            if datum:
                self.shooter.flywheel.spin_to_standby_speed()
        """
        if state_id == "l_y_axis":
            if datum:
                self.pickup.angle_change(datum)

        if state_id == "r_shoulder":
            if datum:
                self.pickup.roll(1.0)
            else:
                self.pickup.stop()
        if state_id == "l_shoulder":
            if datum:
                self.pickup.roll(-1.0)
            else:
                self.pickup.stop()
        if state_id == "r_x_axis":
            if datum:
                self.manual_shooter.turn(datum*.3)
        if state_id == "x_button":
            if datum:
                #self.manual_shooter.spin_flywheel(1.0)
                self.pickup.zero()
        if state_id == "y_button":
            if datum:
                self.pickup.go_to_zero()
                #self.manual_shooter.spin_flywheel(0)
        if state_id == "b_button":
            if datum:
                #self.manual_shooter.shooter_down()
                print("Going Back")
                self.pickup.go_back()
            # else:
            #     pass
                #self.manual_shooter.shooter_up()
        if state_id == "a_button":
            if datum:
                print("Going to Portcullis")
                self.pickup.go_to_portcullis()
        







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