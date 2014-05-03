import requests
import pprint
import cStringIO

PAGE_SIZE=1024*1024 # 1 mb

class PageCacheURL:
    def __init__(self, base_url, page_size = PAGE_SIZE):
        self.base_url = base_url
        self.page_size = PAGE_SIZE
        r = requests.options(base_url)
        self.options = r.headers
        
    def __getitem__(self, key):
        
        raise NotImplementedError

    def get_page(self, page_number):
        start = self.page_size * page_number
        end = start + self.page_size
        headers = dict(Range = "bytes=%s-%s" % (start, end))
        r = requests.get(self.base_url, headers = headers)
        if r.status_code not in (
                requests.codes.ok,
                requests.codes.partial_content):
            raise KeyError(r)
        return r.content

pcu = PageCacheURL("http://localhost/test.bin")
pprint.pprint(pcu.options)
t = pcu.get_page(0)
s = cStringIO.StringIO(t)
