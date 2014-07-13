cimport numpy as np
import numpy as np
import mmap
cdef sigsegv_dispatcher thingking_dispatch
cdef mmap_object my_mmap

cdef int handler(void *fault_address, void *user_arg):
    print "Fault address", <np.int64_t> (fault_address - <void*>my_mmap.data)

def setup(mmap_obj, page_to_protect):
    if not isinstance(mmap_obj, mmap.mmap):
        raise RuntimeError
    sigsegv_init(&thingking_dispatch)
    cdef sigsegv_area_handler_t h = handler
    global my_mmap
    my_mmap = mmap_obj
    sigsegv_register(&thingking_dispatch, my_mmap.data, my_mmap.size,
                     &handler, &my_mmap)
    mprotect(<void *>my_mmap.data, my_mmap.size, PROT_READ)
