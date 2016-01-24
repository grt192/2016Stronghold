class Rails:
    def __init__(self, shooter):
        self.shooter = shooter
        self.rails_actuator = shooter.rails_actuator

    def rails_up(self):
        self.rails_actuator.set(False)

    def rails_down(self):
        self.rails_actuator.set(True)
