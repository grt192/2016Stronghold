from wpilib import CANTalon


class OverrideManager:
    pickup_override = True
    tt_override = True
    hood_override = True
    vt_override = True
    
    def __init__(self, shooter, pickup, compressor):
        self.shooter = shooter
        self.pickup = pickup
        self.shooter.override_manager = self
        self.pickup.override_manager = self
        self.shooter.hood.override_manager = self
        self.shooter.turntable.override_manager = self

    def vt_alt(self):
        self.vt_override = True

    def vt_norm(self):
        self.vt_override = False

    def turntable_alt(self):
        self.tt_override = True
        self.shooter.turntable.disable_front_lock()

    def turntable_norm(self):
        self.tt_override = False
        self.shooter.turntable.enable_front_lock()

    def hood_alt(self):
        self.hood_override = True
        self.shooter.hood.disable_automatic_control()

    def hood_norm(self):
        self.hood_override = False
        #HOOD_MIN = 155
        #HOOD_MAX = 385
        self.shooter.hood.enable_automatic_control()

    def pickup_alt(self):
        self.pickup_override = True
        self.pickup.disable_automatic_control()

    def pickup_norm(self):
        self.pickup_override = False
        self.pickup.enable_automatic_control()

    def compressor_alt(self):
        self.compressor.stop()

    def compressor_norm(self):
        self.compressor.start()


        