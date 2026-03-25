import numpy as np


def mirror_field(landscape):
    """
    Creates mirrored version of the field (second 'snake')
    """
    mirrored = np.flipud(landscape)
    return mirrored


def combine_fields(field_a, field_b, mode="difference"):
    """
    Combine original + mirrored field
    """

    if mode == "difference":
        return field_a - field_b

    elif mode == "sum":
        return field_a + field_b

    elif mode == "product":
        return field_a * field_b

    else:
        raise ValueError("Unknown mode")
