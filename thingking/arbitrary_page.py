import requests
import pprint
import io
from math import ceil, floor
try:
    from functools import lru_cache
except ImportError:
    try:
        from functools32 import lru_cache
    except ImportError:
        raise
import numpy as np
import logging

rlogger = logging.getLogger("requests.packages.urllib3.connectionpool")
rlogger.setLevel('WARNING')

PAGE_SIZE=1024*1024 # 1 mb
MAX_PAGES=4*1024 # 1 gb

class PageCacheURL:
    """
    This class sets up a mechanism for caching pages from a URL, using HTTP
    range queries and an LRU-cache for invalidating cached sections of the
    page.  base_url refers to the URL for the page which we'll be
    incrementally caching, and page_size is the size (in bytes) of the page
    chunks that are cached.  By default, the number of pages cached is
    1024, which means up to 1 gigabyte by default.
    """
    def __init__(self, base_url, page_size = PAGE_SIZE):
        self.base_url = base_url
        self.page_size = page_size
        r = requests.options(base_url)
        self.options = r.headers
        self.n_read = 0
        # For debugging
        self.last_r = r

        headers = {'Range':"bytes=%s-%s" % (0, 1)}
        r = requests.get( self.base_url, headers=headers)
        try:
            self.total_size = int(r.headers['content-range'].split('/')[-1])
        except:
            # Because it's not there ...
            self.total_size = int(r.headers['content-length'])
            rlogger.warning("Cannot use range requests on %s", self.base_url)
            self.page_size = self.total_size

    def __getitem__(self, key):
        if isinstance(key, tuple):
            start, stop = key
        elif isinstance(key, (int, np.integer)):
            start, stop = key, key + 1
        elif isinstance(key, slice):
            start = key.start
            stop = key.end
        else:
            raise NotImplementedError
        # We assume this is in bytes
        page_start = int(floor(float(start) / self.page_size))
        offset = start % self.page_size
        page_end = int(ceil(float(stop) / self.page_size))
        output = io.BytesIO()
        total_length = stop - start
        for i in range(page_start, page_end):
            end = min(self.page_size, stop-i*self.page_size)
            page = self.get_page(i)
            output.write(page[offset:end])
            offset = 0
        output.seek(0)
        return output.read()

    def get_current_page(self, position):
        """
        This function returns the starting position and the page at a given
        position.
        """
        page = int(floor(float(position) / self.page_size))
        start = page*self.page_size 
        return start, self.get_page(page)

    @lru_cache(MAX_PAGES)
    def get_page(self, page_number):
        """
        This returns a particular page, by page number.
        """
        start = self.page_size * page_number
        end = start + self.page_size
        headers = {'Range': "bytes=%s-%s" % (start, end)}
        r = requests.get(self.base_url, headers = headers)
        if r.status_code not in (
                requests.codes.ok,
                requests.codes.partial_content):
            raise KeyError(r)
        self.n_read += 1
        # For debugging
        self.last_r = r
        return r.content

if __name__ == "__main__":
    pcu = PageCacheURL("http://localhost/test.bin")
    pprint.pprint(pcu.options)
    t = pcu.get_page(0)
    s = io.BytesIO(t)
    print(pcu[:2199])
    data = pcu[2199:2199+128*128*64*32]
    print(pcu.n_read)
    data = pcu[2199:2199+128*128*64*32]
    print(pcu.n_read)
    print(len(data), 128*128*64*32, len(data) - 128*128*64*32)
    arr = np.fromstring(data, dtype=np.dtype([('index', 'i8'),
                                              ('x', '<f4'), ('y', '<f4'), ('z', '<f4'),
                                              ('vx', '<f4'), ('vy', '<f4'), ('vz', '<f4')]))
    print(arr['x'])
