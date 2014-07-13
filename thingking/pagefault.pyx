cimport numpy as np
import numpy as np
import mmap
cdef sigsegv_dispatcher thingking_dispatch
cdef object my_mmap_obj
cdef mmap_object my_mmap

cdef int handler(void *fault_address, int serious):
    return sigsegv_dispatch(&thingking_dispatch, fault_address);

cdef int fault_handler(void *fault_address, void *user_arg):
    print "Fault address", <np.int64_t> (fault_address - <void*>my_mmap.data)
    return 1

def setup(mmap_obj, page_to_protect):
    cdef int rv
    if not isinstance(mmap_obj, mmap.mmap):
        raise RuntimeError
    sigsegv_init(&thingking_dispatch)
    sigsegv_install_handler(&handler)
    global my_mmap, my_mmap_obj
    my_mmap_obj = mmap_obj
    my_mmap = (<mmap_object*> (<PyObject*> mmap_obj))[0]
    sigsegv_register(&thingking_dispatch, my_mmap.data, my_mmap.size,
                     &fault_handler, &my_mmap)
    print "RV2", rv
    rv = mprotect(<void *> my_mmap.data, my_mmap.size, PROT_NONE)
    print "RV3", rv
