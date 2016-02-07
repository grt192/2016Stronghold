class MechController:

    def __init__(self, driver_joystick, xbox_controller, switch_panel, pickup, shooter, operation_manager): # mechanisms belong in arguments
        # define mechanisms here
        

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        
        self.pickup = pickup
        self.shooter = shooter
        self.operation_manager = operation_manager
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)
        switch_panel.add_listener(self._switch_panel_listener)


    def _xbox_controller_listener(self, sensor, state_id, datum):
        if self.pickup_override:
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

        if self.tt_override:
            if state_id == "r_x_axis":
                if datum:
                    self.shooter.turntable.turn(datum*.3)

        if state_id == "l_trigger":
            if datum < .5:
                if self.vt_override:
                    self.operation_manager.geo_automatic_shot()
                else:
                    self.operation_manager.vt_automatic_shot()

        if state_id == "r_trigger":
            if datum < .5:
                self.operation_manager.automatic_pickup()


        if state_id == "x_button":
            if datum:
                self.shooter.flywheel.speed_increment_function()
        if state_id == "y_button":
            if datum:
                self.shooter.flywheel.speed_decrement_function()


        if state_id == "a_button":
            if datum:
                self.pickup.go_to_frame_position()

        if state_id == "b_button":
            if datum:
                self.operation_manager.automatic_pickup_shot_abort()
        

    def _switch_panel_listener(self, sensor, state_id, datum):
        pass






    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == "button2":
            if datum:
                self.operation_manager.cross_pickup_in()
            else:
                self.operation_manager.cross_abort()

        if state_id == "button3":
            if datum:
                self.operation_manager.cross_pickup_out()
            else:
                self.operation_manager.cross_abort()


        if state_id == "button4":
            if datum:
                if self.vt_override:
                    self.operation_manager.geo_automatic_shot()
                else:
                    self.operation_manager.vt_automatic_shot()
        if state_id == "button5":
            if datum:
                self.shooter.abort_automatic_pickup_shot()

        

        if state_id == "button8":
            if datum:
                self.operation_manager.chival_cross()
            else:
                self.operation_manager.chival_cross_abort()
        