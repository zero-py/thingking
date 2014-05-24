import requests
import pprint
import cStringIO
from math import ceil, floor
from functools32 import lru_cache
import numpy as np

from arbitrary_page import PageCacheURL, PAGE_SIZE, MAX_PAGES


class HTTPArray(PageCacheURL):

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
        if not isinstance(key, slice):
            raise NotImplementedError

        #print 'Keys: %i, %i' % (key.start, key.stop)
        #print 'Itemsize: %i, header_offset: %i' % (self.itemsize, self.header_offset)
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
        #print 'Reading from %i to %i' % (byte_start, byte_end)
        raw_data = self.pcu[byte_start:byte_end]
        arr = np.fromstring(raw_data, dtype=self.dtype)
        return arr

