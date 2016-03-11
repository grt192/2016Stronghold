"""
Module for various drivetrain control mechanisms.
Listens to Attack3Joysticks, not wpilib.Joysticks.
"""


class ArcadeDriveController:
    """
    Class for controlling DT in arcade drive mode, with one or two joysticks.
    """

    def __init__(self, dt, l_joystick, shooter, r_joystick=None):
        """
        Initialize arcade drive controller with a DT and up to two joysticks.
        """
        self.dt = dt
        self.l_joystick = l_joystick
        self.r_joystick = r_joystick
        shooter.drivecontroller = self
        shooter.dt = self.dt
        self.manual_control_enabled = True
        self.l_joystick.add_listener(self._joylistener)
        if self.r_joystick:
            self.r_joystick.add_listener(self._joylistener)



    def _joylistener(self, sensor, state_id, datum):
        if sensor in (self.l_joystick, self.r_joystick) and state_id in ('x_axis', 'y_axis'):
                if self.manual_control_enabled:
                    if abs(self.l_joystick.x_axis) > .03 or abs(self.l_joystick.y_axis) > .03:
                        power = self.l_joystick.y_axis
                        turnval = self.l_joystick.x_axis#self.r_joystick.x_axis if self.r_joystick else self.l_joystick.x_axis
                        # get turn value from r_joystick if it exists, else get it from l_joystick
                        self.dt.set_dt_output(power + turnval,
                                              power - turnval)
                    else:
                        self.dt.set_dt_output(0, 0)
        # elif sensor == self.l_joystick and state_id == 'trigger':
        elif sensor == self.l_joystick and state_id == 'button9':
            if datum:
                self.dt.downshift()
                self.dt.enable_protective_measures()
            else:
                self.dt.upshift()
                self.dt.disable_protective_measures()

        

    def enable_manual_control(self):
        self.manual_control_enabled = True
    def disable_manual_control(self):
        self.manual_control_enabled = False


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
