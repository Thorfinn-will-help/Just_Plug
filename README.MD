# Just Plug

Turn your RC transmitter into a PC joystick for flight simulators using an ESP32.

Just Plug is an open-source bridge between RC radio systems and PC flight simulators. It reads channel data from a receiver connected to an ESP32, processes and calibrates the inputs, and outputs them as a virtual joystick using vJoy.

The goal is simple: allow RC pilots to practice in simulators using their actual transmitter instead of a keyboard, gamepad, or expensive USB trainer cable.

---

## Features

* ESP32-based receiver interface
* Automatic serial port detection
* Real-time channel monitoring
* Channel calibration system
* Persistent calibration storage
* Deadzone support
* Channel normalization
* Axis reversal
* vJoy integration
* 4-axis support
* Windows GUI
* Simulator compatibility

Supported controls:

* Aileron
* Elevator
* Throttle
* Rudder

---

## How It Works

```text
RC Transmitter
      │
      ▼
 RC Receiver
      │
      ▼
    ESP32
      │
      ▼
 Just Plug
      │
      ▼
    vJoy
      │
      ▼
 Flight Simulator
```

The receiver sends channel information to the ESP32.

The ESP32 forwards channel data through USB serial.

Just Plug reads the serial data, applies calibration, deadzones, normalization, and optional axis reversal.

The processed values are sent to a virtual joystick through vJoy.

Any simulator that supports joystick input can then use the transmitter as a controller.

---

## Hardware Requirements

### Required

* ESP32 DevKit V1
* RC transmitter
* RC receiver capable of iBUS output
* USB cable
* Windows PC

### Tested Hardware

Transmitter:

* FlySky FS-i6

Receiver:

* FlySky FS-iA6B

Microcontroller:

* ESP32 DevKit V1

---

## Software Requirements

Install the following before running Just Plug:

### Python

Python 3.10 or newer

### vJoy

Install vJoy before running the application.

Without vJoy, Windows will not receive the virtual joystick output.

---

## Receiver Wiring

### FlySky FS-iA6B

Connect the iBUS signal pin from the receiver to:

```text
ESP32 GPIO16 (RX2)
```

Connect power and ground:

```text
Receiver VCC  -> ESP32 5V
Receiver GND  -> ESP32 GND
```

---

## ESP32 Firmware

The ESP32 firmware reads iBUS data from the receiver and sends channel values over serial.

Example output:

```text
1500,1500,1000,1500
```

Channel order:

```text
CH1 = Aileron
CH2 = Elevator
CH3 = Throttle
CH4 = Rudder
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Thorfinn-will-help/Just_Plug.git
```

### Install Dependencies

```bash
pip install pyserial
pip install pyvjoy
pip install PyQt6
```

### Run

```bash
python main.py
```

---

## Building the Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed --name JustPlug main.py
```

Executable will be created inside:

```text
dist/
```

---

## First Time Setup

### Step 1

Install vJoy.

### Step 2

Connect ESP32.

### Step 3

Turn on transmitter.

### Step 4

Launch Just Plug.

### Step 5

Press Connect.

### Step 6

Verify channel values are changing.

### Step 7

Calibrate all channels.

### Step 8

Save calibration.

### Step 9

Open simulator and select vJoy device.

---

## Calibration System

Each channel stores:

```text
Minimum
Center
Maximum
```

Calibration data is saved automatically and loaded on startup.

Stored settings include:

* Min value
* Center value
* Max value
* Axis reversal state

---

## Deadzone System

Deadzones remove small stick jitters around center.

Benefits:

* Stable center position
* Reduced noise
* Better simulator control

---

## Normalization

Raw transmitter values are converted into a common range:

```text
-100 to +100
```

This allows different transmitters and receivers to behave consistently.

---

## Axis Reversal

Each channel can be reversed independently.

Supported channels:

* Aileron
* Elevator
* Throttle
* Rudder

---

## Simulator Compatibility

Tested with:

* PicaSim

Other simulators supporting standard Windows joysticks should also work.

Examples:

* RealFlight
* Phoenix RC
* AeroFly RC
* ClearView RC

---

## Project Structure

```text
Just_Plug
│
├── Backend
│   ├── calibration.py
│   ├── channel_data.py
│   ├── deadzone.py
│   ├── esp32_detector.py
│   ├── normalization.py
│   ├── profile_manager.py
│   ├── serial_reader.py
│   ├── vjoy_mapper.py
│   └── vjoy_output.py
│
├── gui
│   └── main_window.py
│
├── profiles
│
├── firmware
│
├── main.py
│
├── README.md
│
└── LICENSE
```

---

## Known Limitations

* Windows only
* Requires vJoy installation
* Currently supports iBUS receivers
* Single transmitter profile

---

## Future Plans

* Automatic calibration wizard
* Multiple profile support
* Firmware upload through GUI
* Additional receiver protocols
* Expanded simulator testing
* Installer package

---

## Contributing

Bug reports, feature requests, and pull requests are welcome.

---

## License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

## Author

GitHub:

Thorfinn-will-help
*ChatGPT*

Built for RC pilots who would rather fly than spend money on proprietary simulator adapters.

