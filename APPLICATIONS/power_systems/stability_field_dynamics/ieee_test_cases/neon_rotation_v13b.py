import numpy as np


def inject_neon_rotation(Fx, Fy, strength=0.25):
    """
    Inject rotational (curl-like) component into the flow field.
    This creates vortices / loops → "neon channel".

    Parameters:
        Fx, Fy : flow field components
        strength : rotation strength

    Returns:
        Fx_new, Fy_new
    """

    # compute gradients
    dFy_dx = np.gradient(Fy, axis=1)
    dFx_dy = np.gradient(Fx, axis=0)

    # curl approximation
    curl = dFy_dx - dFx_dy

    # rotate field (perpendicular component)
    rot_x = -np.gradient(curl, axis=0)
    rot_y =  np.gradient(curl, axis=1)

    Fx_new = Fx + strength * rot_x
    Fy_new = Fy + strength * rot_y

    return Fx_new, Fy_new
