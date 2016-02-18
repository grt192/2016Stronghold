class Rails:
    def __init__(self, rails_actuator):
        self.rails_actuator = rails_actuator
        self.isUp = True

    def rails_up(self):
        self.rails_actuator.set(False)
        self.isUp = True

    def rails_down(self):
        self.rails_actuator.set(True)
        self.isUp = False
