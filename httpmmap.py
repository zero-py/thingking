import numpy as np
from arbitrary_page import PageCacheURL, PAGE_SIZE


class HTTPArray(object):

    """docstring for HTTPArray"""

    def __init__(self, base_url, dtype=None, offset=0, shape=None,
                 order='C', page_size=PAGE_SIZE):
        self.base_url = base_url
        if dtype is None:
            dtype = np.dtype([("data", "|S1")])
        self.dtype = dtype
        self.header_offset = offset
        if shape is not None:
            shape = int(shape)
        self.shape = shape
        self.order = None
        self.itemsize = self.dtype.itemsize
        self.pcu = PageCacheURL(base_url, page_size=page_size)

    def __getitem__(self, key):
        mask = None
        if type(key) == np.ndarray:
            mask = key
            key = slice(None, None)
        if not isinstance(key, slice):
            raise NotImplementedError

        if key.start is None:
            key = slice(0, key.stop)
        if key.stop is None:
            key = slice(key.start, self.shape)
        if key.start < 0:
            key = slice(self.shape + key.start, key.stop)
        if key.stop < 0:
            key = slice(key.start, self.shape + key.stop)
        byte_start = self.header_offset + key.start*self.itemsize
        byte_end = self.header_offset + key.stop*self.itemsize
        raw_data = self.pcu[byte_start:byte_end]
        arr = np.fromstring(raw_data, dtype=self.dtype)
        if mask is None:
            return arr
        else:
            return arr[mask]

