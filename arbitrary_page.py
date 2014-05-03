import requests
import pprint
import cStringIO
from math import ceil, floor
from functools32 import lru_cache

PAGE_SIZE=1024*1024 # 1 mb
MAX_PAGES=1024 # 1 gb

class PageCacheURL:
    def __init__(self, base_url, page_size = PAGE_SIZE):
        self.base_url = base_url
        self.page_size = PAGE_SIZE
        r = requests.options(base_url)
        self.options = r.headers
        self.n_read = 0
        
    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise NotImplementedError
        # We assume this is in bytes
        page_start = int(floor(float(key.start) / self.page_size))
        offset = key.start % self.page_size
        end = min(self.page_size, key.stop)
        page_end = int(ceil(float(key.stop) / self.page_size))
        output = cStringIO.StringIO()
        for i in range(page_start, page_end):
            page = self.get_page(i)
            output.write(page[offset:end])
            offset = 0
            end = min(self.page_size, key.stop - output.tell())
        output.seek(0)
        return output.read()

    @lru_cache(MAX_PAGES)
    def get_page(self, page_number):
        start = self.page_size * page_number
        end = start + self.page_size
        headers = dict(Range = "bytes=%s-%s" % (start, end))
        r = requests.get(self.base_url, headers = headers)
        if r.status_code not in (
                requests.codes.ok,
                requests.codes.partial_content):
            raise KeyError(r)
        self.n_read += 1
        return r.content

pcu = PageCacheURL("http://localhost/test.bin")
pprint.pprint(pcu.options)
t = pcu.get_page(0)
s = cStringIO.StringIO(t)
print pcu[:2199]

