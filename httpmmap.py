import requests
import pprint
import cStringIO
from math import ceil, floor
from functools32 import lru_cache
import numpy as np

from arbitrary_page import PageCacheURL, PAGE_SIZE, MAX_PAGES


class HTTPArray(PageCacheURL):

    """docstring for HTTPArray"""

    def __init__(self, base_url, dtype='uint8', offset=0, shape=None,
                 order='C', page_size=PAGE_SIZE):
        self.base_url = base_url
        self.page_size = PAGE_SIZE
        r = requests.options(base_url)
        self.options = r.headers
        self.n_read = 0
        self.dtype = dtype
        self.offset = offset
        self.shape = None
        self.order = None
        self.itemsize = self.dtype.itemsize
        self.pcu = PageCacheURL(base_url, page_size=page_size)

    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise NotImplementedError

        byte_start = self.offset + key.start*self.itemsize
        byte_end = self.offset + key.stop*self.itemsize
        raw_data = self.pcu[byte_start:byte_end]
        arr = np.fromstring(raw_data, dtype=self.dtype)
        return arr


