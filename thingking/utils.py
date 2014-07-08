from httpmmap import HTTPArray
from cStringIO import StringIO
import numpy as np

def isurl(path):
    if path.startswith('http://'): return True
    if path.startswith('https://'): return True
    if path.startswith('ftp://'): return True
    if path.startswith('file://'): return True
    return False

def loadtxt(path, **kwargs):
    """
    Load data from a local or remote HTTP file.

    numpy.loadtxt docs:
    """
    if isurl(path):
        data = HTTPArray(path)
        return np.loadtxt(StringIO(data[:]), **kwargs)
    return np.loadtxt(path, **kwargs)
loadtxt.__doc__ += np.loadtxt.__doc__
