Examples
========

``weather.py``: Load up global temperature data from NASA and plot it vs time. 

``apod.py``: Find the current APOD image, and write it out to a local file.  If
you have PIL installed, you could modify to load it up in matplotlib.

``first_web_mmap.py``: This was actually our first attempt to memory map
something on the web. Doesn't actually work unless you put data up at the
specified location.

``second_web_mmap.py``: This was our second attempt, and accesses particle data
from a cosmological simulation that is hosted at NERSC. It then prints out some
information about the particles that are loaded on-demand.
