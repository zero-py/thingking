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
            dtype = np.dtype([("data", np.str)])
        self.dtype = dtype
        self.header_offset = offset
        self.shape = None
        self.order = None
        self.itemsize = self.dtype.itemsize
        self.pcu = PageCacheURL(base_url, page_size=page_size)

    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise NotImplementedError

        #print 'Keys: %i, %i' % (key.start, key.stop)
        #print 'Itemsize: %i, header_offset: %i' % (self.itemsize, self.header_offset)
        byte_start = self.header_offset + key.start*self.itemsize
        byte_end = self.header_offset + key.stop*self.itemsize
        #print 'Reading from %i to %i' % (byte_start, byte_end)
        raw_data = self.pcu[byte_start:byte_end]
        arr = np.fromstring(raw_data, dtype=self.dtype)
        return arr

