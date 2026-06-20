import pyvjoy


class VJoyOutput:

    def __init__(self):

        self.joystick = pyvjoy.VJoyDevice(1)

    def set_axis(
        self,
        x,
        y,
        z,
        rz
    ):

        self.joystick.set_axis(
            pyvjoy.HID_USAGE_X,
            x
        )

        self.joystick.set_axis(
            pyvjoy.HID_USAGE_Y,
            y
        )

        self.joystick.set_axis(
            pyvjoy.HID_USAGE_Z,
            z
        )

        self.joystick.set_axis(
            pyvjoy.HID_USAGE_RZ,
            rz
        )