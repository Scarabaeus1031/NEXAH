import numpy as np


def apply_field_control(states, risk, strength=0.05):
    """
    Simple field-based control.

    Idea:
    Push trajectory slightly away from high-risk regions
    using gradient approximation.

    Parameters
    ----------
    states : np.ndarray (T, N)
    risk : np.ndarray (T,)
    strength : float

    Returns
    -------
    controlled_states : np.ndarray (T, N)
    """

    controlled = states.copy()

    # gradient of risk (1D over time)
    grad = np.gradient(risk)

    for t in range(1, len(states)):
        direction = -grad[t]  # move away from increasing risk

        # apply small correction along state direction
        controlled[t] = controlled[t] + strength * direction

    return controlled
