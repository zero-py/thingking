from thingking.httpmmap import HTTPArray, httpfile
import re

apod = httpfile("http://apod.nasa.gov/apod/")
for all_l in apod.readlines():
    for l in all_l.split("\n"):
        if 'IMG SRC' in l:
            good_line = l

#Find the image
url = re.search('\"(.*?)\"', good_line.split("=")[1]).group(1)
ext = url.split('.')[-1]

# Load into HTTPArray
img = HTTPArray(apod.name + url)

# write it out.
f = open("apod_today.%s" % ext, 'wb')
f.write(img[:].data[:])
f.close()
