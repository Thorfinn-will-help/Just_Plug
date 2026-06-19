import json



PROFILE_FILE = "profiles/calibration.json"


def save_calibration(data):

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

        print("Loading:", PROFILE_FILE)
        with open(
            PROFILE_FILE,
            "r"
        ) as file:

            data = json.load(file)

            print("Loaded:", data)

            return data

    except Exception as e:

        print("LOAD ERROR:", e)

        return {
            "aileron": {},
            "elevator": {},
            "throttle": {},
            "rudder": {}
        }