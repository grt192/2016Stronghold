from wpilib import Talon
from wpilib import PIDController


class DriveTrain:
    """
    Standard 6-motor drivetrain, with standard tankdrive.
    """
    power = 1.0
    LOW_GEAR_RAMP_RATE = 2

    def __init__(self,
                 left_motor, right_motor,
                 left_shifter=None, right_shifter=None,
                 left_encoder=None, right_encoder=None):
        """
        Initializes the drivetrain with some motors (or MotorSets),
        optional shifters and encoders
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.left_shifter = left_shifter
        self.right_shifter = right_shifter
        self.left_encoder = left_encoder
        self.right_encoder = right_encoder
        self.dt_left = self.left_motor
        self.dt_right = self.right_motor


    def set_dt_output(self, left_output, right_output):
        """
        Sets the DT output values; should be between -1 and 1.
        """
        left_output *= self.power
        right_output *= self.power
        self.left_motor.set(-left_output)
        self.right_motor.set(+right_output)

    def enable_protective_measures(self):
        self.left_motor.setVoltageRampRate(self.LOW_GEAR_RAMP_RATE)
        self.right_motor.setVoltageRampRate(self.LOW_GEAR_RAMP_RATE)

    def disable_protective_measures(self):
        self.left_motor.setVoltageRampRate(0)
        self.right_motor.setVoltageRampRate(0)


    def set_right_motor(self, power):
        self.right_motor.set(power)

    def set_left_motor(self, power):
        self.left_motor.set(power)

    def set_power(self, power):
        """
        Sets the power level of the DT (should be between 0-1)
        Scales all the motor outputs by this factor.
        """
        self.power = sorted([0, power, 1])[1]  # clamp :)

    def upshift(self):
        """
        Upshifts, if shifters are present.
        """
        if self.left_shifter:
            self.left_shifter.set(True)
        if self.right_shifter:
            self.right_shifter.set(True)

    def downshift(self):
        """
        Downshifts, if shifters are present.
        """
        if self.left_shifter:
            self.left_shifter.set(False)
        if self.right_shifter:
            self.right_shifter.set(False)
