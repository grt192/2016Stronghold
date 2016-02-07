
from wpilib import Joystick
from grt.core import Sensor

BUTTON_TABLE = ['switch1', 'switch2', 'switch3', 'switch4',
                'switch5', 'switch6', 'switch7',
                'switch8', 'switch9', 'switch10']


class SwitchPanel(Sensor):
    """
    Sensor wrapper for the Switch Panel.
    """

    switch1 = switch2 = switch3 = switch4 = switch5 = switch6 = switch7 = switch8 = switch9 = switch10 = False

    def __init__(self, port):
        """
        Initializes the joystick with some USB port.
        """
        super().__init__()
        self.j = Joystick(port)

    def poll(self):
        for i, state_id in enumerate(BUTTON_TABLE, 1):
            self.update_state(state_id,
                              self.j.getRawButton(i))
            # button index is offset by 1 due to wpilib 1-indexing
