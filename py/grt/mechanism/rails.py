class Rails:
    def __init__(self, rails_actuator):
        self.rails_actuator = rails_actuator
        self.is_up = True

    def rails_up(self):
        self.is_up = True
        self.rails_actuator.set(False)

    def rails_down(self):
        self.is_up = False
        self.rails_actuator.set(True)