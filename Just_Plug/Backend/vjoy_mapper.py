def to_vjoy(value):

    return int(
        ((value + 100) / 200)
        *
        32767
    )