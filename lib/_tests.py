import numpy as np
from functions import *

def test_score_function():
    x = np.array([0, 0, 0, 4, 4, 4])
    assert off_nominal(x) == 0.0, "Test failed"
    print("Test passed")

if __name__ == "__main__":
    test_score_function()