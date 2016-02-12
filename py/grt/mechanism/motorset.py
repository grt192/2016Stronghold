from wpilib import CANTalon


class Motorset:
    """
    Drop-in replacement for wpilib.SpeedController. Useful for grouping
    bunches of motors together.
    """

    @staticmethod
    def group(motors, scalefactors=None):
        """
        Takes a tuple of motors and possibly a tuple of
        scalefactors, with which the motor outputs are multiplied.

        The first motor in motors is Followed by the rest
        """
        num_motors = len(motors)

        if not scalefactors:
            scalefactors = (1,) * num_motors

        if num_motors != len(scalefactors):
            raise ValueError("Scalefactors must have the same number of elements as motors")

        lead_motor = motors[0]

        for i, motor in enumerate(motors):
            motor.changeControlMode(CANTalon.ControlMode.Follower)
            motor.set(lead_motor.getDeviceID())
            if scalefactors[i] < 0:
                motor.reverseOutput(True)