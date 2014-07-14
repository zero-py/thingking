from cpython.ref cimport PyObject, Py_INCREF, Py_DECREF
from libc.stdio cimport FILE, fprintf, stdout, stderr
from libc.stdlib cimport malloc, free

cdef extern from "Python.h":
    PyObject* PyFile_FromFile(FILE *fp, char *name, char *mode,
                              int (*close)(FILE*))

cdef extern from "unistd.h":
    ctypedef unsigned size_t
    ctypedef unsigned ssize_t
    ctypedef signed off_t
    ctypedef signed off64_t

cdef extern from "stdio.h":
    
    cdef int SEEK_SET
    cdef int SEEK_CUR
    cdef int SEEK_END

    ctypedef struct cookie_io_functions_t:
        ssize_t (*read)(void *cookie, char *buf, size_t size) nogil
        ssize_t (*write)(void *cookie, const char *buf, size_t size) nogil
        int (*seek)(void *cookie, off64_t *offset, int whence) nogil
        int (*close)(void *cookie) nogil

    cdef FILE *fopencookie(void *cookie, const char *mode,
                           cookie_io_functions_t io_funcs) nogil
