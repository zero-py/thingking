#include <Python.h>
#include <fcntl.h>
// This duplicates some of the mmapmodule.c file.

typedef enum
{
    ACCESS_DEFAULT,
    ACCESS_READ,
    ACCESS_WRITE,
    ACCESS_COPY
} access_mode;

typedef struct {
    PyObject_HEAD
    char *      data;
    size_t      size;
    size_t      pos;    /* relative to offset */
    off_t       offset;

    int fd;

    access_mode access;
} mmap_object;
