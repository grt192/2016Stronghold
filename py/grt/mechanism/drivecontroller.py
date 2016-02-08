"""
Module for various drivetrain control mechanisms.
Listens to Attack3Joysticks, not wpilib.Joysticks.
"""


class ArcadeDriveController:
    """
    Class for controlling DT in arcade drive mode, with one or two joysticks.
    """

    def __init__(self, dt, l_joystick, straight_macro=None, r_joystick=None):
        """
        Initialize arcade drive controller with a DT and up to two joysticks.
        """
        self.dt = dt
        self.l_joystick = l_joystick
        self.r_joystick = r_joystick
        self.l_joystick.add_listener(self._joylistener)
        if self.r_joystick:
            self.r_joystick.add_listener(self._joylistener)

        self.straight_macro = straight_macro

        #self.engage()

    def _joylistener(self, sensor, state_id, datum):
        if sensor in (self.l_joystick, self.r_joystick) and state_id in ('x_axis', 'y_axis'):
            if not self.straight_macro.enabled:
                power = self.l_joystick.y_axis
                turnval = self.l_joystick.x_axis#self.r_joystick.x_axis if self.r_joystick else self.l_joystick.x_axis
                # get turn value from r_joystick if it exists, else get it from l_joystick
                self.dt.set_dt_output(power + turnval,
                                      power - turnval)
        elif sensor == self.l_joystick and state_id == 'trigger':
            if datum:
                self.dt.upshift()
            else:
                self.dt.downshift()

        elif sensor == self.l_joystick and state_id == "button6":
            if datum:
                self.straight_macro.enable()
            else:
                self.straight_macro.disable()
        elif state_id == "button7":
            if datum:
                self.straight_macro.disable()
                self.dt.set_dt_output(0, 0)

    #def _vision_listener(self, sensor, state_id, datum):


    #def engage(self):
            

    #def disengage(self):
    #        self.l_joystick.remove_listener(self._joylistener)
    #        if self.r_joystick:
    #            self.r_joystick.remove_listener(self._joylistener)

class TankDriveController:
    """
    Class for controlling DT in tank drive mode with two joysticks.
    """

    def __init__(self, dt, l_joystick, r_joystick):
        """
        Initializes self with a DT and left and right joysticks.
        """
        self.dt = dt
        self.l_joystick = l_joystick
        self.r_joystick = r_joystick
        l_joystick.add_listener(self._joylistener)
        r_joystick.add_listener(self._joylistener)

    def _joylistener(self, sensor, state_id, datum):
        if sensor in (self.l_joystick, self.r_joystick) and state_id in ('x_axis', 'y_axis'):
            self.dt.set_dt_output(self.l_joystick.y_axis,
                                  self.r_joystick.y_axis)
