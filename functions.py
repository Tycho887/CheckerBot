import numpy as np
import sqlite3


def score(input_vector):

    assert isinstance(input_vector, np.ndarray), "input vector must be a numpy array"
    assert len(input_vector) == 5, "input vector must have 6 elements"
    # assert all(isinstance(i, int) for i in input_vector), "input vector must contain only integers"
    assert all(i >= 1 for i in input_vector), "values must be greater than 1"
    assert all(i <= 5 for i in input_vector), "values must be less than or equal to 5"

    ideal_vector, weights = np.array([5,5,5,1,1]), np.array([5,3,1,1,1])
    
    # the process is split into stages for readability

    first = lambda vector: np.linalg.norm(weights * (vector-ideal_vector)) # find the distance
    second = lambda vector: first(vector) / first(np.array([1,1,1,5,5])) # normalize the distance
    third = lambda vector: 1-second(vector) # invert the distance

    score_function = lambda vector: 100*(third(vector))**2 # map the values

    return score_function(input_vector)

if __name__ == "__main__":
    print(score(np.array([5,5,5,1,1],dtype=int))) # 100.0
    print(score(np.array([5,5,5,5,5],dtype=int))) # 0.0
    print(score(np.array([2,5,5,5,5],dtype=int))) # 0.0
    print(score(np.array([1,1,1,5,5],dtype=int))) # 50.0