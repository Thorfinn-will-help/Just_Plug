import sys
import time

from Backend.deadzone import apply_deadzone
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui.main_window import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()

last_data_time = 0


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