
from grt.sensors.ticker import Ticker
import numpy as np
from wpilib import SmartDashboard

class NTTicker(Ticker):
    DURATION = .25

    def __init__(self, shooter, pickup, straight_macro):
        super().__init__(self.DURATION)
        self.shooter = shooter
        self.pickup = pickup
        self.straight_macro = straight_macro
        SmartDashboard.putDouble("HLower", self.shooter.robot_vision.getLowerThreshold()[0])
        SmartDashboard.putDouble("SLower", self.shooter.robot_vision.getLowerThreshold()[1])
        SmartDashboard.putDouble("VLower", self.shooter.robot_vision.getLowerThreshold()[2])
        SmartDashboard.putDouble("HUpper", self.shooter.robot_vision.getUpperThreshold()[0])
        SmartDashboard.putDouble("SUpper", self.shooter.robot_vision.getUpperThreshold()[1])
        SmartDashboard.putDouble("VUpper", self.shooter.robot_vision.getUpperThreshold()[2])

        SmartDashboard.putDouble("TURNTABLE_KP", self.shooter.turntable.TURNTABLE_KP)
        SmartDashboard.putDouble("TURNTABLE_KI", self.shooter.turntable.TURNTABLE_KI)
        SmartDashboard.putDouble("TURNTABLE_KD", self.shooter.turntable.TURNTABLE_KD)


    def tick(self):
        h_lower = SmartDashboard.getDouble("HLower")
        s_lower = SmartDashboard.getDouble("SLower")
        v_lower = SmartDashboard.getDouble("VLower")
        h_upper = SmartDashboard.getDouble("HUpper")
        s_upper = SmartDashboard.getDouble("SUpper")
        v_upper = SmartDashboard.getDouble("VUpper")
        self.shooter.robot_vision.setThreshold(np.array([h_lower, s_lower, v_lower], 'uint8'), np.array([h_upper, s_upper, v_upper], 'uint8'))

        self.shooter.turntable.TURNTABLE_KP = SmartDashboard.getDouble("TURNTABLE_KP")
        self.shooter.turntable.TURNTABLE_KI = SmartDashboard.getDouble("TURNTABLE_KI")
        self.shooter.turntable.TURNTABLE_KD = SmartDashboard.getDouble("TURNTABLE_KD")


