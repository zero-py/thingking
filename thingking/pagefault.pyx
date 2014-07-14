import sys, time
from thingking.httpmmap import httpfile

cdef object cookies = {}

cdef ssize_t tk_read(void *cookie, char *buf, size_t size) nogil:
    global cookies
    cdef int i
    cdef ssize_t osize
    cdef char* b
    with gil:
        tk_obj = cookies[(<int*>cookie)[0]]
        s = tk_obj.read(int(size))
        b = s
        osize = len(s)
    for i in range(osize):
        buf[i] = b[i]
    return osize

cdef ssize_t tk_write(void *cookie, const char *buf, size_t size) nogil:
    # We do not allow writing.
    return 0

cdef int tk_seek(void *cookie, off64_t *offset, int whence) nogil:
    global cookies
    cdef int rv
    with gil:
        tk_obj = cookies[(<int*>cookie)[0]]
        rv = tk_obj.seek(offset[0], whence)
        offset[0] = tk_obj._cpos
    return rv

cdef int tk_close(void *cookie) nogil:
    # We only decref
    with gil:
        del cookies[(<int*>cookie)[0]]

cdef cookie_io_functions_t tk_cookie_funcs
tk_cookie_funcs.read = tk_read
tk_cookie_funcs.write = tk_write
tk_cookie_funcs.seek = tk_seek
tk_cookie_funcs.close = tk_close

def thingking_to_FILE(tk):
    if not isinstance(tk, httpfile):
        raise RuntimeError
    cdef int* cookie = <int*> malloc(sizeof(int))
    cookie[0] = len(cookies)
    cookies[cookie[0]] = tk
    cdef FILE *nf = fopencookie(<void *> cookie, "rb", tk_cookie_funcs)
    cdef object f = <object>PyFile_FromFile(nf, tk.name, "rb", NULL)
    return f
