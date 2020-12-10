import numpy as np

def iterate_randomly_over_all_cells(array: np.array):
    """
    A generator for values and coordinates in the given array. Will loop
    through all cells within the array randomly, returning each once.
    Parameters
    ----------
    array : np.array
        A multi-dimensional numpy array
    Returns
    -------
    coordinate: tuple
        A tuple of the index of a cell in the array, with a 2D array this would
        be (x, y), where the value can be retrieved with array[coordinate]
    """
    coords = list(np.ndindex(array.shape))
    np.random.shuffle(coords)
    for coord in coords:
        yield coord