__author__ = "Chelay and Neelimay"

from _init_.py import Challoopa
from turntable.py import TurnTable

class MechController:

    def __init__(self, driver_joystick, xbox_controller, swtich_controller, shooter, belt_roller_motor, rails_actuator,challoopa): # mechanisms belong in arguments
        # define mechanisms here
        self.rails_actuator = rails_actuator
        self.shooter = shooter
        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        self.belt_roller_motor = belt_roller_motor
        self.challoopa = challoopa
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)
        driver_swtichjoystick_listener.add_listener(self._driver_swtichjoystick_listener)


    def _xbox_controller_listener(self, sensor, state_id, datum):
        if state_id == "x_button":
            if datum:
                self.shooter.flywheel_motor.set(-1)
        if state_id == "y_button":
            if datum:
                self.shooter.flywheel_motor.set(1)
        if state_id == "b_button":
            if datum:
                self.challoopa.extend(datum)
            else:
                self.challoopa.extend(0)
        if state_id == "a_button":
            if datum:
                self.challoopa.back(datum)
        if state_id == "r_trigger":
            if datum:
                self.rails_actuator.set(False)
        if state_id == "l_trigger":
            if datum:
                self.rails_actuator.set(True)
        if state_id == "r_button":
            if datum:
                self.spin_forward(datum)
        if state_id == "l_button":
            if datum:
                 self.spin_backwards(datum)
        if state_id == "r_stick":
            if datum:
                self.turntable.turn(datum)
        if state_id == "l_y_axis":
            if datum:
                self.challoopa.extend(datum)


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

    def _driver_swtichjoystick_listener(self, sensor, state_id, datum):
            if state_id == "button1":
                if datum:
                    print("button1 on")
                else 
                    print("button1 off")
            if state_id == "button2":
                if datum:
                    print("button2 on")
                else 
                    print("button2 off")
            if state_id == "button3":
                if datum:
                    print("button3 on")
                else 
                    print("button3 off")
            if state_id == "button4":
                if datum:
                    print("button4 on")
                else 
                    print("button5 off")
            if state_id == "button1":
                if datum:
                    print("button5 on")
                else 
                    print("button5 off")
            if state_id == "button6":
                if datum:
                    print("button6 on")
                else 
                    print("button6 off")
            if state_id == "button7":
                if datum:
                    print("button7 on")
                else 
                    print("button7 off")
            if state_id == "button8":
                if datum:
                    print("button8 on")
                else 
                    print("button8 off")
            if state_id == "button9":
                if datum:
                    print("button9 on")
                else 
                    print("button9 off")





