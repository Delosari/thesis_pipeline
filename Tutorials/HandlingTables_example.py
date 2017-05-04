import string
import numpy as np    
import bisect
    
f = open("/home/vital/Dropbox/Astrophysics/Lore/NebularContinuum/t5_elec.ascii")
a = f.readlines()
f.close()

nTe = int(string.split(a[0])[0])                   # number of Te columns
print nTe                                          #76

nener = int(string.split(a[0])[1])                 # number of energy points rows
print nener                                        #323

skip = int(1+np.ceil(nTe/8.))
print skip                                         #11

temp = np.zeros(nTe)
for i in range(1,skip) :
    tt = string.split(a[i])
    for j in range(0,len(tt)) :
        temp[8*(i-1)+j] = tt[j]
        
print temp

Te = 10500

print bisect.bisect_right(temp,np.log10(Te))

print bisect.bisect_left(temp,np.log10(Te))

#If value not in list => bisect_left = bisect_right
#If value not in list => bisect_left coordinate of the good column

rte2 = 0
if bisect.bisect_right(temp,np.log10(Te)) - bisect.bisect_left(temp,np.log10(Te)) == 1 : 
    rte1 = bisect.bisect_left(temp,np.log10(Te))  # Te existe
    print rte1,rte2
elif bisect.bisect_right(temp,np.log10(Te)) - bisect.bisect_left(temp,np.log10(Te)) == 0 :
    rte1 = bisect.bisect_left(temp,np.log10(Te))-1 # interpola Te
    rte2 = bisect.bisect_right(temp,np.log10(Te))  # 
    print rte1,rte2
else :
    print 'ERROR IN Te COLUMN DETECTION FOR Gamma_fb'