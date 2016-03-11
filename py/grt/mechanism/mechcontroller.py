class MechController:
    

    def __init__(self, driver_joystick, xbox_controller, switch_panel, pickup, shooter, operation_manager, override_manager, pickup_macro=None): # mechanisms belong in arguments
        # define mechanisms here
        

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        
        self.pickup = pickup
        self.shooter = shooter
        self.operation_manager = operation_manager
        self.override_manager = override_manager
        self.pickup_macro = pickup_macro



        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)
        switch_panel.add_listener(self._switch_panel_listener)


    def _xbox_controller_listener(self, sensor, state_id, datum):
        """
        Pickup angle change manual control
        """
        if self.override_manager.pickup_override:
            if state_id == "l_y_axis":
                if datum:
                    print("Moving pickup")
                    self.pickup.angle_change(datum)
                
            

        """
        Turntable rotation manual control
        """
        if self.override_manager.tt_override:
            if state_id == "r_x_axis":
                if datum:
                    self.shooter.turntable.turn(datum*.3)

        """
        Hood rotation manual control
        """
        if self.override_manager.hood_override:
            if state_id == "r_y_axis":
                if datum:
                    self.shooter.hood.rotate(-datum*.3)

        """
        Pickup operation
        """
        if state_id == "r_shoulder":
            if self.pickup_macro:
                if datum:
                    self.pickup_macro.macro_initialize()
                else:
                    self.pickup_macro.terminate()
            else:
                if datum:
                    self.operation_manager.manual_pickup()
                else:
                    self.operation_manager.manual_pickup_abort()

        """
        Run roller in reverse
        """
        if state_id == "l_shoulder":
            if datum:
                self.pickup.roll(-2.0)
            else:
                self.pickup.roll(0)

        """
        Abort a shot
        """
        if state_id == "l_trigger":
            if datum > .7:
                self.operation_manager.shot_abort()

        """
        Start an automatic shot. Shot type depends on which switches are pressed
        """
        if state_id == "r_trigger":
            if datum > .7:
                if self.override_manager.vt_override:
                    self.operation_manager.geo_automatic_shot()
                else:
                    self.operation_manager.vt_automatic_shot()


        """
        Increment the flywheel speed. Only affects the value for the currently selected shot type.
        """
        if state_id == "x_button":
            if datum:
                if self.override_manager.vt_override:
                    self.shooter.flywheel.increment_geo_power()
                    self.shooter.flywheel.increment_geo_speed()
                else:
                    self.shooter.flywheel.increment_vt_speed()

        """
        Decrement the flywheel speed. Only affects the value for the currently selected shot type.
        """
        if state_id == "y_button":
            if datum:
                if self.override_manager.vt_override:
                    self.shooter.flywheel.decrement_geo_power()
                    self.shooter.flywheel.decrement_geo_speed()
                else:
                    self.shooter.flywheel.decrement_vt_speed()
                #self.shooter.flywheel.spindown()

        """
        Decrement the offset for the vision-tracking turntable center.
        """
        if state_id == "back_button":
            if datum:
                self.shooter.turntable.decrement_vt_setpoint()

        """
        Increment the offset for the vision-tracking turntable center.
        """
        if state_id == "start_button":
            if datum:
                self.shooter.turntable.increment_vt_setpoint()

        """
        Raise the pickup to the frame position
        """
        if state_id == "a_button":
            if datum:
                self.pickup.go_to_frame_position()

        """
        Lower the pickup to the pickup position
        """
        if state_id == "b_button":
            if datum:
                self.pickup.go_to_pickup_position()
        

    def _switch_panel_listener(self, sensor, state_id, datum):
        """
        Flywheel full reverse power
        """
        if state_id == "switch2":
            if datum:
                self.shooter.flywheel.spin_to_full_reverse_power()
            else:
                self.shooter.flywheel.spindown()
        """
        Flywheel full forward power
        """
        if state_id == "switch5":
            if datum:
                self.shooter.flywheel.spin_to_full_power()
            else:
                self.shooter.flywheel.spindown()
        """
        Geo shot select (also overrides vt and flywheel auto-speed-set)
        """
        if state_id == "switch7":
            if datum:
                self.override_manager.vt_alt()
            else:
                self.override_manager.vt_norm()

        
        """
        Turntable auto-zero override (allows Xbox joystick to control turntable)
        """
        if state_id == "switch4":
            if datum:
                self.override_manager.turntable_alt()
                
            else:
                self.override_manager.turntable_norm()
                

        """
        Hood close-loop control override (allows Xbox joystick to control hood)
        """
        if state_id == "switch9":
            if datum:
                self.override_manager.hood_alt()
            else:
                self.override_manager.hood_norm()
        
        """
        Shooter rails manual control
        """
        if state_id == "switch6":
            if datum:
                self.shooter.rails.rails_up()
            else:
                self.shooter.rails.rails_down()

        """
        Pickup close-loop control override (allows Xbox joystick to control pickup)
        """                
        if state_id == "switch8":
            if datum:
                self.override_manager.pickup_alt()
            else:
                self.override_manager.pickup_norm()
        
        """
        Compressor override (used in high-power situations)
        """
        if state_id == "switch3":
            if datum:
                self.override_manager.compressor_alt()
            else:
                self.override_manager.compressor_norm()






    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == "button3":
            if datum:
                self.operation_manager.forward_straight_cross()
            else:
                self.operation_manager.straight_cross_abort()

        if state_id == "button2":
            if datum:
                self.operation_manager.reverse_straight_cross()
            else:
                self.operation_manager.straight_cross_abort()

        

        if state_id == "button4":
            if datum:
                if self.override_manager.vt_override:
                    self.operation_manager.geo_automatic_shot()
                else:
                    self.operation_manager.vt_automatic_shot()

        if state_id == "button5":
            if datum:
                self.operation_manager.shot_abort()

        if state_id == "button6":
            if datum:
                self.operation_manager.chival_cross()
            else:
                self.operation_manager.chival_cross_abort()

        if state_id == "button7":
            pass
            # if datum:
            #     self.operation_manager.portcullis_cross()
            # else:
            #     self.operation_manager.portcullis_cross_abort()

        

        if state_id == "button8":
            if datum:
                self.shooter.rails.rails_down()
            
        if state_id == "button9":
            if datum:
                self.shooter.rails.rails_up()

        elif state_id == "button10":
            if datum:
                self.operation_manager.record_macro.start_record()
            else:
                self.operation_manager.record_macro.stop_record()
            

#Requested driver joystick mappings

#Don't worry about pickup -- just have the Xbox controller move it in if necessary
#Trigger -- shifting
#Button 2 -- straight macro cross using the gyro, does not move the pickup (lower priority on the field-centric obstacle cross alignment)
#Higher priority on the low gear protection ramp rate and on testing the daylight vision settings with non-daylight conditions

#Mess around with multiplicative vs. additive arcade (lower priority)

#Chival macro (raise, forward, down, go)

#Change the default shooter position to down
#When you're ready to pickup or shoot, run the backdrive
#Button 6 -- chival macro
#Button 7 -- portcullis macro

#Button 10 -- recording
#Button 11 -- playback
#Buttons 8 and 9 -- random debugging

#3 switches in a row


#Requested Xbox controller mappings
#Presets:

#Right trigger (RT) -- get vision tracking to lock onto the goal, spin the flywheel to the correct speed, and lower the elevator to shoot (vt_automatic_shot)
#Right shoulder (RB) -- spin chalupa for intake
#Left shoulder (LB) -- spin chalupa in reverse for portcullis
#Left trigger (LT) -- abort failsafe
#Y -- up increment shooter power
#X -- down increment shooter power
#B -- bring chalupa out for pickup
#A -- bring chalupa arm in (decide how much later)

#Manual:

#Right joystick left-right -- rotate the turntable
#Right joystick front-back -- rotate the hood
#Left joystick front-back -- rotate the pickup angle-change

#Switches:
#9 switches arranged in a 3x3 grid on the mech control side

#Also add another display on the mech control



#Cameras:

#One vision-tracking camera mounted in the center of the turret facing forward
#One debugging camera mounted in the center of the turret facing down
#One red dot camera next to the vision-tracking camera facing forward
#Possibly one additonal camera on the drive base


        