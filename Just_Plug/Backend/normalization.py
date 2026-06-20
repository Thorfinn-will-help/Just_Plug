def normalize(
    value,
    minimum,
    center,
    maximum
):

    if value >= center:

        return (
            (value - center)
            /
            (maximum - center)
        ) * 100

    return (
        (value - center)
        /
        (center - minimum)
    ) * 100