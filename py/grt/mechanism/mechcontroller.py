from record_controller import RecordMacro, PlaybackMacro

class MechController:

    def __init__(self, driver_joystick, xbox_controller, record_controller: RecordMacro, playback_macro: PlaybackMacro,  pickup): # mechanisms belong in arguments
        # define mechanisms here
        

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        self.record_controller = record_controller
        self.playback_macro = playback_macro
        self.pickup = pickup
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)


    def _xbox_controller_listener(self, sensor, state_id, datum):

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
        # if state_id == "r_x_axis":
        #     if datum:
        #         self.manual_shooter.turn(datum*.3)
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
                self.pickup.go_back()
            else:
                pass
                #self.manual_shooter.shooter_up()
        if state_id == "a_button":
            if datum:
                self.pickup.go_to_portcullis()
        
    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == "button10":
            if datum:
                print("Recording...")
                self.record_controller.start_record()

            else:
                print("Stopping Recording")
                self.record_controller.stop_record()

        if state_id == "button11":
            if datum:
                print("Playing back...")
                self.playback_macro.start_playback()
            else:
                print("Stopping Playback")
                self.playback_macro.stop_playback()