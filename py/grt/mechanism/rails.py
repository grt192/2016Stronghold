class Rails:
    def __init__(self, rails_actuator):
        self.rails_actuator = rails_actuator

    def rails_up(self):
        self.rails_actuator.set(False)

    def rails_down(self):
        self.rails_actuator.set(True)
