from cpython.ref cimport PyObject
cdef extern from "unistd.h":
    ctypedef unsigned size_t
    ctypedef signed off_t

cdef extern from "signal.h":
    ctypedef void* ucontext_t

cdef extern from "pagefault.h":
    ctypedef enum access_mode:
        ACCESS_DEFAULT
        ACCESS_READ
        ACCESS_WRITE
        ACCESS_COPY

    ctypedef struct mmap_object:
        # Skip the stuff we don't want ...
        char *data
        size_t size
        size_t pos
        off_t offset
        int fd
        access_mode access

cdef extern from "sys/mman.h":
    int mprotect(const void *addr, size_t len, int prot)
    cdef int PROT_NONE
    cdef int PROT_READ
    cdef int PROT_WRITE
    cdef int PROT_EXEC

cdef extern from "sigsegv.h":
    ctypedef int (*sigsegv_handler_t) (void* fault_address, int serious)
    int sigsegv_install_handler (sigsegv_handler_t handler)
    void sigsegv_deinstall_handler ()
    int sigsegv_leave_handler (void (*continuation) (void*, void*, void*), void* cont_arg1, void* cont_arg2, void* cont_arg3)
    void sigsegv_leave_handler ()
    ctypedef ucontext_t *stackoverflow_context_t
    ctypedef void (*stackoverflow_handler_t) (int emergency, stackoverflow_context_t scp)
    int stackoverflow_install_handler (stackoverflow_handler_t handler,
                                            void* extra_stack, unsigned long extra_stack_size)
    void stackoverflow_deinstall_handler ()
    ctypedef int (*sigsegv_area_handler_t) (void* fault_address, void* user_arg)
    ctypedef struct sigsegv_dispatcher:
        void* tree
    void sigsegv_init (sigsegv_dispatcher* dispatcher)
    void* sigsegv_register (sigsegv_dispatcher* dispatcher,
                            void* address, unsigned long len,
                            sigsegv_area_handler_t handler, void* handler_arg)
    void sigsegv_unregister (sigsegv_dispatcher* dispatcher, void* ticket)
    int sigsegv_dispatch (sigsegv_dispatcher* dispatcher, void* fault_address)

