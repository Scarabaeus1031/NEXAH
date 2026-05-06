# test_kernel_bridge.py
import pytest
import numpy as np

def test_example():
    phase_history = np.random.rand(100, 100)
    assert phase_history.shape == (100, 100)
