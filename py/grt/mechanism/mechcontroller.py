
from grt.sensors.dummy import Mimic
import math

class MechController:
    def __init__(self, driver_joystick, xbox_controller, shooter, robot_vision, dummy_vision=False):  # mechanisms belong in arguments
        # define mechanisms here
        self.shooter = shooter

        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        self.robot_vision = robot_vision
        self.dummy_vision = dummy_vision

        driver_joystick.add_listener(self._driver_joystick_listener)
        driver_joystick.add_listener(self._dummy_vision_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)

    def _dummy_vision_listener(self, sensor, state_id, datum):
        # If robot_vision is a Mimic
        if type(self.robot_vision) == Mimic:
            if state_id == "button2":
                # print("----Setting Target View----")
                self.robot_vision.target_view = datum
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
            if datum:
                print("Target View:", self.robot_vision.target_view,
                      "Rotational Error:", self.robot_vision.rotational_error,
                      "Vertical Error:", self.robot_vision.vertical_error)

    def _xbox_controller_listener(self, sensor, state_id, datum):

        if state_id == "x_button":
            if datum:
                self.shooter.flywheel.increment_speed()
        if state_id == "y_button":
            if datum:
                self.shooter.flywheel.decrement_speed()
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
