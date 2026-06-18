def normalize(
    raw,
    min_value,
    center_value,
    max_value
):

    if raw <= center_value:

        return map_range(
            raw,
            min_value,
            center_value,
            1000,
            1500
        )

    else:

        return map_range(
            raw,
            center_value,
            max_value,
            1500,
            2000
        )
def map_range(
    value,
    in_min,
    in_max,
    out_min,
    out_max
):

    return (
        (value - in_min)
        *
        (out_max - out_min)
        /
        (in_max - in_min)
        +
        out_min
    )