"""
Module for various drivetrain control mechanisms.
Listens to Attack3Joysticks, not wpilib.Joysticks.
"""


class ArcadeDriveController:
    """
    Class for controlling DT in arcade drive mode, with one or two joysticks.
    """

    def __init__(self, dt, l_joystick, shooter, r_joystick=None, xbox_joystick=None):
        """
        Initialize arcade drive controller with a DT and up to two joysticks.
        """
        self.dt = dt
        self.l_joystick = l_joystick
        self.r_joystick = r_joystick
		self.xbox_joystick = xbox_joystick
		if self.xbox_joystick:
			self.xbox_joystick.add_listener(self._cheesydrivelistener)
        shooter.drivecontroller = self
        shooter.dt = self.dt
        self.manual_control_enabled = True
        self.l_joystick.add_listener(self._joylistener)
        if self.r_joystick:
            self.r_joystick.add_listener(self._joylistener)


	def _cheesydrivelistener(self, sensor, state_id, datum):
		if sensor is self.xbox_joystick and state_id in ("l_y_axis", "r_x_axis"):
			throttle = sensor.l_y_axis
			wheel = sensor.r_x_axis
			isQuickTurn = sensor.r_shoulder
			isHighGear = True
			
			oldWheel = None
			quickStopAccumulator = None
			throttleDeadband = 0.02
			wheelDeadband = 0.02
			
			def limit(v, limit):
				return v if (abs(v) < limit) else limit * (-1 if v < 0 else 1)
				
			def handleDeadband(val, deadband):
				return val if (abs(val) > abs(deadband)) else 0.0

			#double wheelNonLinearity

			wheel = handleDeadband(wheel, wheelDeadband)
			throttle = handleDeadband(throttle, throttleDeadband)

			negInertia = wheel - oldWheel
			oldWheel = wheel

			if isHighGear:
				wheelNonLinearity = 0.6
				# Apply a sin function that's scaled to make it feel better.
				wheel = math.sin(math.PI / 2.0 * wheelNonLinearity * wheel)
						/ math.sin(math.PI / 2.0 * wheelNonLinearity)
				wheel = math.sin(math.PI / 2.0 * wheelNonLinearity * wheel)
						/ math.sin(math.PI / 2.0 * wheelNonLinearity)
			else:
				wheelNonLinearity = 0.5
				# Apply a sin function that's scaled to make it feel better.
				wheel = math.sin(math.PI / 2.0 * wheelNonLinearity * wheel)
						/ math.sin(math.PI / 2.0 * wheelNonLinearity)
				wheel = math.sin(math.PI / 2.0 * wheelNonLinearity * wheel)
						/ math.sin(math.PI / 2.0 * wheelNonLinearity)
				wheel = math.sin(math.PI / 2.0 * wheelNonLinearity * wheel)
						/ math.sin(math.PI / 2.0 * wheelNonLinearity)
			

			#double leftPwm, rightPwm, overPower
			#double sensitivity

			#double angularPower
			#double linearPower

			# Negative inertia!
			negInertiaAccumulator = 0.0
			
			if isHighGear:
				negInertiaScalar = 4.0
				sensitivity = .75 #Constants.kDriveSensitivity
			else:
				if (wheel * negInertia > 0):
					negInertiaScalar = 2.5
				else:
					if (math.abs(wheel) > 0.65):
						negInertiaScalar = 5.0
					else:
						negInertiaScalar = 3.0
						
				sensitivity = .85 #Constants.sensitivityLow.getDouble()
			
			negInertiaPower = negInertia * negInertiaScalar
			negInertiaAccumulator += negInertiaPower

			wheel = wheel + negInertiaAccumulator
			if (negInertiaAccumulator > 1):
				negInertiaAccumulator -= 1
			elif (negInertiaAccumulator < -1):
				negInertiaAccumulator += 1
			else:
				negInertiaAccumulator = 0
				
			linearPower = throttle

			# Quickturn!
			if isQuickTurn:
				if (abs(linearPower) < 0.2):
					alpha = 0.1
					quickStopAccumulator = (1 - alpha) * quickStopAccumulator
							+ alpha * limit(wheel, 1.0) * 5
				
				overPower = 1.0
				if isHighGear:
					sensitivity = 1.0
				else:
					sensitivity = 1.0
				
				angularPower = wheel
			else:
				overPower = 0.0
				angularPower = abs(throttle) * wheel * sensitivity
						- quickStopAccumulator
				if (quickStopAccumulator > 1):
					quickStopAccumulator -= 1
				else if (quickStopAccumulator < -1):
					quickStopAccumulator += 1
				else:
					quickStopAccumulator = 0.0

			rightPwm = leftPwm = linearPower
			leftPwm += angularPower
			rightPwm -= angularPower

			if (leftPwm > 1.0):
				rightPwm -= overPower * (leftPwm - 1.0)
				leftPwm = 1.0
			else if (rightPwm > 1.0):
				leftPwm -= overPower * (rightPwm - 1.0)
				rightPwm = 1.0
			else if (leftPwm < -1.0):
				rightPwm += overPower * (-1.0 - leftPwm)
				leftPwm = -1.0
			else if (rightPwm < -1.0):
				leftPwm += overPower * (-1.0 - rightPwm)
				rightPwm = -1.0
			
			self.dt.set_dt_output(leftPwm, rightPwm)
			

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
                pass
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
