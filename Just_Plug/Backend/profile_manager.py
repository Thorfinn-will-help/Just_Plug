import json
import os


APP_DIR = os.path.join(
    os.getenv("APPDATA"),
    "JustPlug"
)

PROFILE_FILE = os.path.join(
    APP_DIR,
    "calibration.json"
)


def save_calibration(data):

    os.makedirs(
        APP_DIR,
        exist_ok=True
    )

    with open(
        PROFILE_FILE,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


def load_calibration():

    try:

        print(
            "Loading:",
            PROFILE_FILE
        )

        with open(
            PROFILE_FILE,
            "r"
        ) as file:

            data = json.load(file)

            print(
                "Loaded:",
                data
            )

            return data

    except Exception as e:

        print(
            "LOAD ERROR:",
            e
        )

        return {
            "aileron": {},
            "elevator": {},
            "throttle": {},
            "rudder": {}
        }