import sys
import time

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

    selected_channel = (
        window.calibration_channel.currentText()
    )

    window.current_raw_label.setText(
        f"Current Raw: {data[selected_channel]}"
    )
    window.current_raw_value = data[selected_channel]

    window.signal_label.setText(
        "Signal: OK"
    )


timer = QTimer()
timer.timeout.connect(update_channels)
timer.start(8)

sys.exit(app.exec())