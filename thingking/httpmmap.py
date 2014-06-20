import numpy as np
from arbitrary_page import PageCacheURL, PAGE_SIZE
import warnings
from numpy import uint8, ndarray, dtype
import sys
from io import BufferedReader, BufferedIOBase
import array

import numpy as np

dtypedescr = dtype


class HTTPArray(object):

    """docstring for HTTPArray"""

    def __init__(self, base_url, dtype=None, offset=0, shape=None,
                 order='C', page_size=PAGE_SIZE):
        self.base_url = base_url
        if dtype is None:
            dtype = np.dtype([("data", "|S1")])
        self.dtype = dtype
        self.header_offset = offset
        self.order = None
        self.itemsize = self.dtype.itemsize
        self.pcu = PageCacheURL(base_url, page_size=page_size)
        if shape is not None:
            shape = int(shape)
        else:
            shape = self.pcu.total_size/self.itemsize
        self.shape = shape

    def __getitem__(self, key):
        mask = None
        kt = type(key)
        if kt == int or kt == np.int64 or kt == np.int32 or kt == np.int:
            if key == -1:
                key = slice(-1, None)
            else:
                key = slice(key, key+1)
        elif type(key) == np.ndarray:
            # We do it all here.
            arr = np.empty(key.size, dtype=self.dtype)
            for i, v in enumerate(key):
                byte_start = self.header_offset + v * self.itemsize
                byte_end = byte_start + self.itemsize
                arr[i] = np.fromstring(self.pcu[byte_start:byte_end],
                                dtype=self.dtype)
            return arr
        if not isinstance(key, slice):
            raise NotImplementedError

        if key.start is None:
            key = slice(0, key.stop)
        if key.stop is None:
            key = slice(key.start, self.shape)
        if key.start < 0:
            key = slice(self.shape + key.start, key.stop)
        if key.stop < 0:
            key = slice(key.start, self.shape + key.stop)
        byte_start = self.header_offset + key.start*self.itemsize
        byte_end = self.header_offset + key.stop*self.itemsize
        raw_data = self.pcu[byte_start:byte_end]
        arr = np.fromstring(raw_data, dtype=self.dtype)
        if mask is None:
            return arr
        else:
            return arr[mask]


class httpfile(object):
    """docstring for httpfile"""
    closed = False
    _cpos = 0  # Current position
    writeable = False
    mode = "r"

    def __init__(self, base_url, page_size=PAGE_SIZE):
        self.pcu = PageCacheURL(base_url, page_size=page_size)
        self.size = self.pcu.total_size
        self.name = base_url

    def fileno(self):
        """docstring for fileno"""
        return -1

    def readable(self):
        """docstring for readable"""
        return True

    def seekable(self):
        """docstring for readable"""
        return True

    def close(self):
        """
        Closes the mmap. Subsequent calls to other methods of the object will
        result in a ValueError exception being raised. This will not close the
        open file.  """
        self.closed = True

    def find(self, string, start=0, end=-1):
        """
        Returns the lowest index in the object where the substring string is
        found, such that string is contained in the range [start, end].
        Optional arguments start and end are interpreted as in slice notation.
        Returns -1 on failure.
        """
        return -1

    def flush(self, offset=None, size=None):
        """
        Flushes changes made to the in-memory copy of a file back to disk.
        Without use of this call there is no guarantee that changes are written
        back before the object is destroyed. If offset and size are specified,
        only changes to the given range of bytes will be flushed to disk;
        otherwise, the whole extent of the mapping is flushed.

        (Windows version): A nonzero value returned indicates success; zero
        indicates failure.

        (Unix version): A zero value is returned to indicate success. An exception is raised when the call failed.
        """
        pass

    def move(self, dest, src, count):
        """
        Copy the count bytes starting at offset src to the destination index
        dest. If the mmap was created with ACCESS_READ, then calls to move will
        raise a TypeError exception.
        """
        raise NotImplementedError()

    def read(self, num):
        """
        Return a string containing up to num bytes starting from the current
        file position; the file position is updated to point after the bytes
        that were returned.
        """
        start = self._cpos
        end = min(self._cpos+num, self.size)
        print 'Reading from %i to %i' % (start, end)
        data = self.pcu[start:end]
        self._cpos = end
        return data

    def read1(self, ):
        return self.read(1)

    def readinto(self, b):
        return len(b)

    def peek(self, num, offset=0):
        """
        Return a string containing up to num bytes starting from the current
        file position; the file position is updated to point after the bytes
        that were returned.
        """
        start = self._cpos+offset
        end = min(self._cpos+offset+num, self.size)
        data = self.pcu[start:end]
        return data

    def read_byte(self):
        """
        Returns a string of length 1 containing the character at the current
        file position, and advances the file position by 1.
        """
        return self.read(1)

    def readline(self):
        """
        Returns a single line, starting at the current file position and up to
        the next newline.
        """
        tmp = 1 * self._cpos
        chunksize = 1024
        data = ''
        readsize = 0
        while True:
            chunk = self.peek(chunksize, offset=readsize)
            data += chunk
            newline = chunk.find("\n")
            if newline != 0:
                readsize += newline
                break
            else:
                readsize += len(chunk)
        data = self.pcu[self._cpos:self._cpos+readsize]
        self._cpos += readsize + 1
        return data

    def readlines(self):
        """
        Returns a single line, starting at the current file position and up to
        the next newline.
        """
        while self._cpos < self.size:
            yield self.readline()

    def resize(self, newsize):
        """
        Resizes the map and the underlying file, if any. If the mmap was
        created with ACCESS_READ or ACCESS_COPY, resizing the map will raise
        a TypeError exception.
        """
        raise TypeError()

    def rfind(self, string, start=None, end=None):
        """
        Returns the highest index in the object where the substring string is
        found, such that string is contained in the range [start, end].
        Optional arguments start and end are interpreted as in slice notation.
        Returns -1 on failure.
        """
        raise NotImplementedError()

    def seek(self, pos, whence=0):
        """
        Set the files current position. whence argument is optional and
        defaults to os.SEEK_SET or 0 (absolute file positioning); other values
        are os.SEEK_CUR or 1 (seek relative to the current position) and
        os.SEEK_END or 2 (seek relative to the files end).
        """
        if whence == 0:
            self._cpos = pos
        elif whence == 1:
            self._cpos += pos
        elif whence == 2:
            raise NotImplementedError()
        else:
            raise NotImplementedError()

    def size(self):
        """
        Return the length of the file, which can be larger than the size of the
        memory-mapped area.
        """
        pass

    def tell(self, ):
        """
        Returns the current position of the file pointer.
        """
        return self._cpos

    def write(self, string):
        """
        Write the bytes in string into memory at the current position of the
        file pointer; the file position is updated to point after the bytes
        that were written. If the mmap was created with ACCESS_READ, then
        writing to it will raise a TypeError exception.
        """
        raise NotImplementedError()

    def write_byte(self, byte):
        """
        Write the single-character string byte into memory at the current
        position of the file pointer; the file position is advanced by 1. If
        the mmap was created with ACCESS_READ, then writing to it will raise
        a TypeError exception.
        """
        raise NotImplementedError()


