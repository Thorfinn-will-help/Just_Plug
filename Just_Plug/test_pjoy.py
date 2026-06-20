import pyvjoy
import time

j = pyvjoy.VJoyDevice(1)

while True:
    j.set_axis(
        pyvjoy.HID_USAGE_X,
        32767
    )
    time.sleep(1)

    j.set_axis(
        pyvjoy.HID_USAGE_X,
        0
    )
    time.sleep(1)