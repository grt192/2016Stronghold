import wpilib

ENC_MIN = 50
ENC_MAX = 51


class TurnTable:

    class PIDVisionSource(wpilib.interfaces.PIDSource):
        """
        PIDSource for turning; uses gyro angle as feedback.
        """

        def __init__(self, vision_mechanism):
            super().__init__()
            self.vision_mechanism = vision_mechanism
            #self.setPIDSourceType(wpilib.interfaces.PIDSource.PIDSourceType.kDisplacement)

        def pidGet(self):
            print("Inputing", self.vision_mechanism.vision_sensor.rotational_error)
            return self.vision_mechanism.vision_sensor.rotational_error

        def getPIDSourceType(self):
            return wpilib.interfaces.PIDSource.PIDSourceType.kDisplacement


    class PIDVisionOutput(wpilib.interfaces.PIDOutput):
        def __init__(self, turntable):
            super().__init__()
            self.turntable = turntable

        def pidWrite(self, output):
            # self.vision_macro.set_output
            # self.turn_macro.dt.set_dt_output(output, -output)
            # self.turntable.turn(output)
            print("Outputing ", output)
            self.turntable.dt_turn(output)

    def __init__(self, motor: wpilib.CANTalon, vision_mechanism, dt=None):
        self.motor = motor
        self.vision_mechanism = vision_mechanism
        self.dt = dt
        self.PID_source = self.PIDVisionSource(vision_mechanism)
        self.PID_output = self.PIDVisionOutput(self)  # It is intentional that the turntable passes itself to
                                                      # the PID output.

        self.PID_controller = wpilib.PIDController(1, 0, 0, self.PID_source, self.PID_output)
        self.PID_controller.setOutputRange(-1, 1)
        self.PID_controller.setAbsoluteTolerance(50)
        self.PID_controller.setSetpoint(0)

    def turn(self, output):
        enc_pos = self.motor.getEncPosition()
        if enc_pos > ENC_MIN and enc_pos < ENC_MAX:
            self.motor.set(output)
        else:
            self.motor.set(0)

    def dt_turn(self, output):
        if self.dt:
            self.dt.set_dt_output(output, -output)

    def turn_to(self, target):
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.motor.setP(1)
        self.motor.set(target) # TODO: WILL NOT CHANGE CONTROL MODE BACK

    def disable(self):
        pass
        #self.motor.disable()
        #self.motor.disableControl()
