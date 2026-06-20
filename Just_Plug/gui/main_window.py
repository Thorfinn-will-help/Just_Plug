from Backend.esp32_detector import get_available_ports
from Backend.serial_reader import SerialReader
from Backend.profile_manager import (
    save_calibration,
    load_calibration
)
from PyQt6.QtWidgets import (
    QGroupBox,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QCheckBox,

)   


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.reverse_aileron = QCheckBox(
         "Reverse Aileron"
        )

        self.reverse_elevator = QCheckBox(
            "Reverse Elevator"
        )

        self.reverse_throttle = QCheckBox(
            "Reverse Throttle"
        )

        self.reverse_rudder = QCheckBox(
            "Reverse Rudder"
        )
        
        self.calibration_group = QGroupBox(
            "Calibration"
        ) 
        self.calibration_channel = QComboBox()
        self.calibration_channel.addItems([
            "aileron",
            "elevator",
            "throttle",
            "rudder"
        ])
        print(
         self.calibration_channel.count()
        )

        self.calibration_values = load_calibration()

        self.current_raw_label = QLabel(
            "Current Raw: 0"
        )
        self.normalized_label = QLabel(
            "Normalized: 0.0"
        )

        self.min_label = QLabel(
            "Stored Min: -"
        )

        self.center_label = QLabel(
            "Stored Center: -"
        )

        self.max_label = QLabel(
            "Stored Max: -"
        ) 
        self.save_button = QPushButton(
            "Save Calibration"
        )
        self.capture_min_button = QPushButton(
            "Capture Min"
        )

        self.capture_center_button = QPushButton(
            "Capture Center"
        )

        self.capture_max_button = QPushButton(
            "Capture Max"
        )

        self.reader = None
        self.current_raw_value = 0



        self.setWindowTitle(
            "RC Simulator Adapter"
        )
        cal_layout = QVBoxLayout()

        cal_layout.addWidget(
        self.calibration_channel
        )
        
        cal_layout.addWidget(
        self.save_button
        )

        cal_layout.addWidget(
        self.current_raw_label
        )
       
        cal_layout.addWidget(
            self.normalized_label
        )

        cal_layout.addWidget(
        self.min_label
        )

        cal_layout.addWidget(
        self.center_label
        )

        cal_layout.addWidget(
        self.max_label
        )
        cal_layout.addWidget(
        self.capture_min_button
        )

        cal_layout.addWidget(
        self.capture_center_button
        )

        cal_layout.addWidget(
        self.capture_max_button
        )

        self.calibration_group.setLayout(
        cal_layout
        )
        cal_layout.addWidget(
            self.reverse_aileron
        )

        cal_layout.addWidget(
            self.reverse_elevator
        )

        cal_layout.addWidget(
            self.reverse_throttle
        )

        cal_layout.addWidget(
            self.reverse_rudder
        )
        
        layout = QVBoxLayout()

        self.port_box = QComboBox()
        
        


        self.refresh_button = QPushButton(
            "Refresh Ports"
        )

        self.connect_button = QPushButton(
            "Connect"
        )
        self.disconnect_button = QPushButton(
        "Disconnect"
        )

        self.status_label = QLabel(
            "Disconnected"
        )
        self.signal_label = QLabel(
         "Signal: LOST"
        )

        self.aileron_label = QLabel(
            "Aileron: 0"
        )

        self.elevator_label = QLabel(
            "Elevator: 0"
        )

        self.throttle_label = QLabel(
            "Throttle: 0"
        )

        self.rudder_label = QLabel(
            "Rudder: 0"
        )

        layout.addWidget(self.port_box)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)

        layout.addWidget(self.status_label)
        layout.addWidget(self.signal_label)
        layout.addWidget(self.aileron_label)
        layout.addWidget(self.elevator_label)
        layout.addWidget(self.throttle_label)
        layout.addWidget(self.rudder_label)
        layout.addWidget(
        self.calibration_group
        )

        self.setLayout(layout)

        self.calibration_channel.currentTextChanged.connect(
            self.update_calibration_display
        )

        self.capture_min_button.clicked.connect(
            self.capture_min
        )
        self.save_button.clicked.connect(
          self.save_profile
        )

        self.capture_center_button.clicked.connect(
            self.capture_center
        )

        self.capture_max_button.clicked.connect(
            self.capture_max
        )

        self.refresh_button.clicked.connect(
            self.refresh_ports
        )

        self.connect_button.clicked.connect(
            self.connect_device
        )
        self.disconnect_button.clicked.connect(
            self.disconnect_device         
        )

        self.refresh_ports()
        print(self.calibration_values)
        self.update_calibration_display()

    def get_selected_port(self):

        return self.port_box.currentText()

    def refresh_ports(self):

        self.port_box.clear()

        ports = get_available_ports()

        for port in ports:
            self.port_box.addItem(
                port["device"]
            )

    def connect_device(self):


        selected_port = self.port_box.currentText()

        try:

            self.reader = SerialReader()
            self.reader.connect(selected_port)

            self.status_label.setText(
            f"Connected to {selected_port}"
            )

        except Exception:

            self.status_label.setText(
            "Connection Failed"


            )   


    def disconnect_device(self):


        try:

            if  self.reader is not None:

                self.reader.serial_port.close()

                self.reader = None

                self.status_label.setText(
                "Disconnected"
                )

        except Exception:

            self.status_label.setText(
            "Disconnect Failed"
            )


    def capture_min(self):


        channel = self.calibration_channel.currentText()

        self.calibration_values[channel]["min"] = (
        self.current_raw_value
        )
        self.update_calibration_display()

        self.min_label.setText(
        f"Stored Min: {self.current_raw_value}"
        )
        self.update_calibration_display()
        print(self.calibration_values)


    def capture_center(self):


        channel = self.calibration_channel.currentText()

        self.calibration_values[channel]["center"] = (
        self.current_raw_value
        )

        self.center_label.setText(
        f"Stored Center: {self.current_raw_value}"
        )
        self.update_calibration_display()
        print(self.calibration_values)


    def capture_max(self):


        channel = self.calibration_channel.currentText()

        self.calibration_values[channel]["max"] = (
        self.current_raw_value
        )

        self.max_label.setText(
        f"Stored Max: {self.current_raw_value}"
        )
        self.update_calibration_display()
        print(self.calibration_values)

    def update_calibration_display(self):

        channel = self.calibration_channel.currentText()

        values = self.calibration_values.get(
            channel,
            {}
        )

        self.min_label.setText(
            f"Stored Min: {values.get('min', '-')}"
        )

        self.center_label.setText(
            f"Stored Center: {values.get('center', '-')}"
        )

        self.max_label.setText(
            f"Stored Max: {values.get('max', '-')}"
        )
    
    def save_profile(self):

        save_calibration(
        self.calibration_values
        )

        self.status_label.setText(
            "Calibration Saved"
        )    