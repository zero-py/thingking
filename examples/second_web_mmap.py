from thingking import HTTPArray
import numpy as np
from time import time
a = HTTPArray("http://portal.nersc.gov/project/darksky/ds14_a/chunk_halos/ds14_a_10166000.cell",
              dtype=np.dtype([('x',np.float32),
                              ('y',np.float32),
                              ('z',np.float32),
                              ('vx',np.float32),
                              ('vy',np.float32),
                              ('vz',np.float32),
                              ('ident', np.int64)])
              )
N = 1000
t = -time(); sub = a[0:N]; t += time(); print t
print 'Particles loaded: %i out of %i, maximum x position: %e' % \
    (N, a.shape, sub['x'].max())
