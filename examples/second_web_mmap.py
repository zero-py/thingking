from thingking import HTTPArray
import numpy as np
from time import time
a = HTTPArray("http://portal.nersc.gov/project/darksky/ds14_a/chunk_halos/ds14_a_170000_1.0000",
              dtype=np.dtype([('x',np.float32),
                              ('y',np.float32),
                              ('z',np.float32),
                              ('vx',np.float32),
                              ('vy',np.float32),
                              ('vz',np.float32),
                              ('ident', np.int64)])
              )
t = -time(); sub = a[0:int(1e6)]; t += time(); print t
