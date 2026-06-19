from Backend.profile_manager import (
    save_calibration,
    load_calibration
)

data = {
    "aileron": {
        "min": 1000,
        "center": 1500,
        "max": 2000
    }
}

save_calibration(data)

print(load_calibration())