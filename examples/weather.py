import thingking
import matplotlib.pyplot as plt
import re

f = thingking.httpfile("http://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.txt")

date = []
temperature = []
for line in f.readlines():
    if re.search('^[\d]+\w[\d]+\w', line):
        vals = line.split()
        year = float(vals[0])
        for i in range(min(len(vals),12)):
            if vals[i+1][-1] == '*': break
            date.append(year + (i+.5)/12) # middle of each month
            try:
                temperature.append(int(vals[i+1])/100.0)
            except:
                temperature.append(float('NaN'))

plt.plot(date, temperature, 'o')
plt.title("Global Temperature Anomaly")
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly (C)")
plt.show()
