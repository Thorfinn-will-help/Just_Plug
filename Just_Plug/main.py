import sys
import time

from Backend.deadzone import apply_deadzone
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui.main_window import MainWindow
from Backend.normalization import normalize


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