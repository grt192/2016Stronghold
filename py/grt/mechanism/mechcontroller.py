
from grt.sensors.dummy import Mimic
import math

class MechController:
    hood_override = False
    pickup_override = True
    tt_override = True
    vt_override = True

    def __init__(self, driver_joystick, xbox_controller, switch_panel, pickup, shooter, operation_manager, robot_vision, dummy_vision=False): # mechanisms belong in arguments
        # define mechanisms here
        

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        self.robot_vision = robot_vision
        self.dummy_vision = dummy_vision
        
        self.pickup = pickup
        self.shooter = shooter
        self.operation_manager = operation_manager

        self.shooter.turntable.tt_override = self.tt_override


        driver_joystick.add_listener(self._driver_joystick_listener)
        driver_joystick.add_listener(self._dummy_vision_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)
        switch_panel.add_listener(self._switch_panel_listener)

    def _dummy_vision_listener(self, sensor, state_id, datum):
        # If robot_vision is a Mimic
        if type(self.robot_vision) == Mimic:
            # if state_id == "button2":
            #     # print("----Setting Target View----")
            #     self.robot_vision.target_view = datum
            if state_id == "button3":
                # print("----Enabling Turntable PID----")
                if datum:
                    self.shooter.turntable.pid_controller.enable()
            if state_id == "button4":
                # print("----Disabling Turntable PID----")
                if datum:
                    self.shooter.turntable.pid_controller.disable()
            if state_id == "button5":
                # print("----Disabling Turntable PID----")
                self.shooter.vision_sensor.at_speed = datum
            if state_id == "x_axis":
                # print("----Setting Rotational Error----")
                self.robot_vision.rotational_error = int(datum * 200)

            if state_id == "y_axis":
                # print("----Setting Vertical Error----")
                self.robot_vision.vertical_error = int(datum * 200)



    def _xbox_controller_listener(self, sensor, state_id, datum):
        if self.pickup_override:
            if state_id == "l_y_axis":
                if datum:
                    self.pickup.angle_change(datum)


        if self.tt_override:
            if state_id == "r_x_axis":
                if datum:
                    self.shooter.turntable.turn(datum*.3)
        if self.hood_override:
            if state_id == "r_y_axis":
                if datum:
                    self.shooter.hood.turn(datum*.3)

        if state_id == "r_shoulder":
            if datum:
                self.operation_manager.manual_pickup()
            else:
                self.operation_manager.manual_pickup_abort()
        if state_id == "l_shoulder":
            if datum:
                self.pickup.roll(-1.0)
            else:
                self.pickup.roll(0)



        if state_id == "l_trigger":
            if datum < .5:
                self.operation_manager.shot_abort()

        if state_id == "r_trigger":
            if datum < .5:
                if self.vt_override:
                    self.operation_manager.geo_automatic_shot()
                else:
                    self.operation_manager.vt_automatic_shot()


        if state_id == "x_button":
            if datum:
                self.shooter.flywheel.increment_power()
        if state_id == "y_button":
            if datum:
                self.shooter.flywheel.decrement_power()


        if state_id == "a_button":
            if datum:
                self.pickup.go_to_frame()

        if state_id == "b_button":
            if datum:
                self.pickup.go_to_pickup_position()


    def _switch_panel_listener(self, sensor, state_id, datum):
        if state_id == "switch1":
            if datum:
                self.vt_override = True
            else:
                self.vt_override = False
        if state_id == "switch2":
            if datum:
                self.tt_override = True
                self.shooter.turntable.disable_front_lock()
            else:
                self.tt_override = False
                self.shooter.turntable.enable_front_lock()
        if state_id == "switch3":
            if datum:
                self.hood_override = True
                self.shooter.hood.disable_automatic_control()
            else:
                self.hood_override = False
                self.shooter.hood.enable_automatic_control()
        if state_id == "switch4":
            if datum:
                pass
                #Flywheel override not yet implemented

        if state_id == "switch8":
            if datum:
                self.shooter.rails.rails_down()
            else:
                self.shooter.rails.rails_up()
        if state_id == "switch9":
            if datum:
                self.pickup_override = True
            else:
                self.pickup_override = False
        if state_id == "switch10":
            if datum:
                self.master_fault = True
            else:
                self.master_fault = False
        if state_id == "switch11":
            if datum:
                self.power_conserve = True
            else:
                self.power_conserve = False






    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == "button2":
            if datum:
                self.operation_manager.straight_cross()
            else:
                self.operation_manager.straight_cross_abort()



        if state_id == "button4":
            if datum:
                if self.vt_override:
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
            if datum:
                self.operation_manager.portcullis_cross()
            else:
                self.operation_manager.portcullis_cross_abort()



        if state_id == "button8":
            if datum:
                self.shooter.rails.rails_down()

        if state_id == "button9":
            if datum:
                self.shooter.rails.rails_up()


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


