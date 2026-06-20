import sys
import time
import pyvjoy

from Backend.deadzone import apply_deadzone
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui.main_window import MainWindow
from Backend.normalization import normalize
from Backend.vjoy_output import VJoyOutput
from Backend.vjoy_mapper import to_vjoy


app = QApplication(sys.argv)

window = MainWindow()
window.show()
vjoy = VJoyOutput()
print("vJoy initialized")

last_data_time = 0


def get_vjoy_value(
    channel_name,
    data
):

    values = (
        window.calibration_values.get(
            channel_name,
            {}
        )
    )

    if "center" not in values:
        return 16383

    raw_value = data[channel_name]

    deadzone_value = apply_deadzone(
        raw_value,
        values["center"],
        20
    )

    normalized_value = normalize(
        deadzone_value,
        values["min"],
        values["center"],
        values["max"]
    )

    if (
        channel_name == "aileron"
        and
        window.reverse_aileron.isChecked()
    ):
        normalized_value *= -1

    if (
        channel_name == "elevator"
        and
        window.reverse_elevator.isChecked()
    ):
        normalized_value *= -1

    if (
        channel_name == "throttle"
        and
        window.reverse_throttle.isChecked()
    ):
        normalized_value *= -1

    if (
        channel_name == "rudder"
        and
        window.reverse_rudder.isChecked()
    ):
        normalized_value *= -1

    return to_vjoy(
        normalized_value
    )

def update_channels():

    global last_data_time

    if (
        last_data_time > 0
        and
        time.time() - last_data_time > 2
    ):
        window.signal_label.setText(
            "Signal: LOST"
        )

    if window.reader is None:
        return

    data = window.reader.read_channels()

    if not data:
        return
    x = get_vjoy_value(
        "aileron",
        data
    )

    y = get_vjoy_value(
        "elevator",
        data
    )

    z = get_vjoy_value(
        "throttle",
        data
    )

    rz= get_vjoy_value(
        "rudder",
        data
    )
    vjoy.joystick.set_axis(
        pyvjoy.HID_USAGE_X,
        x
    )

    vjoy.joystick.set_axis(
        pyvjoy.HID_USAGE_Y,
        y
    )

    vjoy.joystick.set_axis(
        pyvjoy.HID_USAGE_Z,
        z
    )

    vjoy.joystick.set_axis(
        pyvjoy.HID_USAGE_RZ,
        rz
    )

    channel = (
        window.calibration_channel.currentText()
    )

    values = (
        window.calibration_values.get(
            channel,
            {}
        )
    )

    if "center" in values:

        raw_value = data[channel]

        deadzone_value = apply_deadzone(
            raw_value,
            values["center"],
            20
        )
        normalized_value = normalize(
            deadzone_value,
            values["min"],
            values["center"],
            values["max"]
        )

        if (
            channel == "aileron"
            and
            window.reverse_aileron.isChecked()
        ):
            normalized_value *= -1

        if (
            channel == "elevator"
            and
            window.reverse_elevator.isChecked()
        ):
            normalized_value *= -1

        if (
            channel == "throttle"
            and
            window.reverse_throttle.isChecked()
        ):
            normalized_value *= -1

        if (
            channel == "rudder"
            and
            window.reverse_rudder.isChecked()
        ):
            normalized_value *= -1
        
        vjoy_value = to_vjoy(
            normalized_value
        )

#        if channel == "aileron":

#           vjoy.joystick.set_axis(
#         pyvjoy.HID_USAGE_X,
#          vjoy_value
#        )

        window.normalized_label.setText(
            f"Normalized: {normalized_value:.1f}"
        )

        window.current_raw_value = (
            deadzone_value
        )

        window.current_raw_label.setText(
            f"Current Raw: {deadzone_value}"
        )

    else:

        window.current_raw_value = (
            data[channel]
        )

        window.current_raw_label.setText(
            f"Current Raw: {data[channel]}"
        )

    last_data_time = time.time()

    window.aileron_label.setText(
        f"Aileron: {data['aileron']}"
    )

    window.elevator_label.setText(
        f"Elevator: {data['elevator']}"
    )

    window.throttle_label.setText(
        f"Throttle: {data['throttle']}"
    )

    window.rudder_label.setText(
        f"Rudder: {data['rudder']}"
    )

    window.signal_label.setText(
        "Signal: OK"
    )
timer = QTimer()
timer.timeout.connect(update_channels)
timer.start(8)

sys.exit(app.exec())