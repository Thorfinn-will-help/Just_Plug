import serial


class SerialReader:

    def __init__(self):
        self.serial_port = None

    def connect(self, port, baudrate=115200):
        self.serial_port = serial.Serial(
            port,
            baudrate,
            timeout=0
        )

    def read_channels(self):

        if not self.serial_port:
            return None

        try:
            line = (
                self.serial_port
                .readline()
                .decode(errors="ignore")
                .strip()
            )

            values = line.split(",")

            if len(values) != 4:
                return None

            return {
                "aileron": int(values[0]),
                "elevator": int(values[1]),
                "throttle": int(values[2]),
                "rudder": int(values[3]),
            }

        except Exception:
            return None
        