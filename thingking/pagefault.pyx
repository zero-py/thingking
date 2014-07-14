from thingking.httpmmap import httpfile

cdef ssize_t tk_read(void *cookie, char *buf, size_t size):
    cdef object tk_obj = <object>(<PyObject*> cookie)
    b = tk_obj.read(size)
    for i in range(len(b)):
        buf[i] = b[i]
    return len(b)

cdef ssize_t tk_write(void *cookie, const char *buf, size_t size):
    # We do not allow writing.
    return 0

cdef int tk_seek(void *cookie, off64_t *offset, int whence):
    cdef object tk_obj = <object>(<PyObject*> cookie)
    cdef int rv = tk_obj.seek(offset[0], whence)
    offset[0] = tk_obj._cpos
    return rv

cdef int tk_close(void *cookie):
    # We only decref
    cdef object tk_obj = <object>(<PyObject*>cookie)
    Py_DECREF(tk_obj)

cdef cookie_io_functions_t tk_cookie_funcs
tk_cookie_funcs.read = tk_read
tk_cookie_funcs.write = tk_write
tk_cookie_funcs.seek = tk_seek
tk_cookie_funcs.close = tk_close

def thingking_to_FILE(tk):
    if not isinstance(tk, httpfile):
        raise RuntimeError
    Py_INCREF(tk)
    cdef void* cookie = <void*>(<PyObject*>tk)
    cdef FILE *nf = fopencookie(cookie, "rb", tk_cookie_funcs)
    cdef object f = <object>PyFile_FromFile(nf, tk.name, "rb", NULL)
    return f
