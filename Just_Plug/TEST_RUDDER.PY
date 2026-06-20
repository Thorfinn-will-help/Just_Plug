import pyvjoy
import time

j = pyvjoy.VJoyDevice(1)

value = 0

while True:

    j.set_axis(
        pyvjoy.HID_USAGE_RZ,
        value
    )

    print(value)

    value += 500

    if value > 32767:
        value = 0

    time.sleep(0.1)