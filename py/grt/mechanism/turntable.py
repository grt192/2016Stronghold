import wpilib
from grt.core import Sensor


ENC_MIN = 50
ENC_MAX = 51


class TurnTable:

    

    def __init__(self, shooter):
        self.shooter = shooter
        self.robot_vision = shooter.robot_vision
        self.dt = shooter.dt
        self.PID_source = self.PIDVisionSource(shooter.robot_vision)
        self.PID_output = self.PIDVisionOutput(self)  # It is intentional that the turntable passes itself to
                                                      # the PID output.

        self.PID_controller = wpilib.PIDController(.08, 0, 0, self.get_input, self.set_output)
        self.PID_controller.setAbsoluteTolerance(100)
        self.PID_controller.reset()
        self.PID_controller.setOutputRange(-.2, .2)
        #self.PID_controller.setInputRange(-300, 300)
        #Be sure to use tolerance buffer
        self.PID_controller.setSetpoint(0)

    def get_input(self):
        #print("Inputing", self.robot_vision.rotational_error)
        return self.robot_vision.rotational_error
    def set_output(self, output):
        #print("Outputing ", output)
        self.dt_turn(output)

    def turn(self, output):
        enc_pos = self.motor.getEncPosition()
        if enc_pos > ENC_MIN and enc_pos < ENC_MAX:
            self.motor.set(output)
        else:
            self.motor.set(0)

    def dt_turn(self, output):
        if self.dt:
            if not self.PID_controller.onTarget():
                self.dt.set_dt_output(-output, -output)
            else:
                self.dt.set_dt_output(0, 0)

    def turn_to(self, target):
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.motor.setP(1)
        self.motor.set(target) # TODO: WILL NOT CHANGE CONTROL MODE BACK


    class PIDVisionSource(wpilib.interfaces.PIDSource):
        """
        PIDSource for turning; uses gyro angle as feedback.
        """

        def __init__(self, robot_vision):
            super().__init__()
            self.robot_vision = robot_vision
            #self.setPIDSourceType(wpilib.interfaces.PIDSource.PIDSourceType.kDisplacement)

        def pidGet(self):
            print("Inputing", self.robot_vision.rotational_error)
            return self.robot_vision.rotational_error

        def __call__(self):
            return self.pidGet()

        def getPIDSourceType(self):
            return wpilib.interfaces.PIDSource.PIDSourceType.kDisplacement


    class PIDVisionOutput(wpilib.interfaces.PIDOutput):
        def __init__(self, turntable):
            super().__init__()
            self.turntable = turntable

        def __call__(self, output):
            self.pidWrite(output)

        def pidWrite(self, output):
            # self.vision_macro.set_output
            # self.turn_macro.dt.set_dt_output(output, -output)
            # self.turntable.turn(output)
            print("Outputing ", output)
            self.turntable.dt_turn(output)

class TurnTableSensor(Sensor):
    def __init__(self, turntable):
        super().__init__()
        self.turntable = turntable
    def poll(self):
        self.rotation_ready = self.turntable.PID_controller.onTarget()
