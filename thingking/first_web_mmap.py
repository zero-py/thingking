from httpmmap import HTTPArray
import numpy as np
a = HTTPArray("http://localhost:8000/ds14_a4_256_0256_0.5000", offset=2432+384, dtype=np.dtype([('x',np.float32), ('y',np.float32), ('z',np.float32), ('vx',np.float32), ('vy',np.float32), ('vz',np.float32), ('ident', np.int64)]))
a[0:1]
a['x'][:100]
a['x'][0:100]
a[0:100]['x']
a[0:1000]['x']
a[10000:11000]['x']
a[100000:110000]['x']
a[100000:110000]['x']
%timeit a[0:1000000]['x']
from time import time
t = -time(); sub = a[2e6:3e6]; t += time(); print t
t = -time(); sub = a[int(2e6):int(3e6)]; t += time(); print t
hist -f first_web_mmap.py
