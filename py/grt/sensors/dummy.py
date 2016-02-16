from grt.core import Sensor


class Mimic(Sensor):
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)


class Dummy(Sensor):
    def __init__(self, f, delta=1, start=0):
        """ Sensor which returns dummy values according to a function f(x, delta)"""
        super().__init__()
        self.f = f
        self.delta = delta
        self.last = start
        self.value = start

    def poll(self):
        self.last += self.delta
        # print("Last: ", self.last)
        self.value = self.f(self.last)
        return self.value
