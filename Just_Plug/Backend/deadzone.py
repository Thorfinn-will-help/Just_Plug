def apply_deadzone(
    value,
    center,
    deadzone
):

    if abs(
        value - center
    ) <= deadzone:

        return center

    return value