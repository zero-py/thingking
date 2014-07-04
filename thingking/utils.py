from httpmmap import HTTPArray
from cStringIO import StringIO
import numpy as np

def loadtxt(path, **kwargs):
    """
    Load data from a local or remote HTTP file.

    numpy.loadtxt docs:
    """
    if 'http' in path:
        data = HTTPArray(path)
        return np.loadtxt(StringIO(data[:]), **kwargs)
    return np.loadtxt(path, **kwargs)
loadtxt.__doc__ += np.loadtxt.__doc__
