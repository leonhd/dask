""" A set of NumPy functions to apply per chunk """

from toolz import concat
import numpy as np


def coarsen(reduction, x, axes):
    """ Coarsen array by applying reduction to fixed size neighborhoods

    Parameters
    ----------

    reduction: function
        Function like np.sum, np.mean, etc...
    x: np.ndarray
        Array to be coarsened
    axes: dict
        Mapping of axis to coarsening factor

    Example
    -------

    >>> x = np.array([1, 2, 3, 4, 5, 6])
    >>> coarsen(np.sum, x, {0: 2})
    array([ 3,  7, 11])
    >>> coarsen(np.max, x, {0: 3})
    array([3, 6])

    Provide dictionary of scale per dimension

    >>> x = np.arange(24).reshape((4, 6))
    >>> x
    array([[ 0,  1,  2,  3,  4,  5],
           [ 6,  7,  8,  9, 10, 11],
           [12, 13, 14, 15, 16, 17],
           [18, 19, 20, 21, 22, 23]])

    >>> coarsen(np.min, x, {0: 2, 1: 3})
    array([[ 0,  3],
           [12, 15]])
    """
    # Insert singleton dimensions if they don't exist already
    for i in range(x.ndim):
        if i not in axes:
            axes[i] = 1

    # (10, 10) -> (5, 2, 5, 2)
    newshape = tuple(concat([(x.shape[i] / axes[i], axes[i])
                                for i in range(x.ndim)]))

    return reduction(x.reshape(newshape), axis=tuple(range(1, x.ndim*2, 2)))
