import math
import numpy as np

data=open('/home/vital/Desktop/J14488_like_lc.dat','r')
lines=data.readlines()
data.close()

MJD = []
flux = []
errflux = []
Bin = []
TS = []
A1 = []
errA1 = []
A2 = []
errA2 = []
A3 = []
errA3 = []
A4 = []
errA4 = []
 
for line in lines:
    p = line.split()
    MJD.append(float(p[0]))
    flux.append(float(p[1]))
    errflux.append(float(p[2]))
    Bin.append(float(p[3]))
    TS.append(float(p[4]))
    A1.append(float(p[5]))
    errA1.append(float(p[6]))
    A2.append(float(p[7]))
    errA2.append(float(p[8]))
    A3.append(float(p[9]))
    errA3.append(float(p[10]))
    A4.append(float(p[11]))
    errA4.append(float(p[12]))
 
JD=np.array(MJD)+2400000.5 - 2450000.0
# 
# for i in range(len(JD)):
#     if TS[i] >= 25:
#         f.writelines([str(JD[i]),str(flux[i]),str(errflux[i]),str(Bin[i]),str(TS[i]),str(A1[i]),str(errA1[i]),str(A2[i]),str(errA2[i]),str(A3[i]),str(errA3[i]),str(A4[i]),str(errA4[i])+"\n"])
#     if TS[i] >= 9:
#         g.writelines([str(JD[i]),str(flux[i]),str(errflux[i]),str(Bin[i]),str(TS[i]),str(A1[i]),str(errA1[i]),str(A2[i]),str(errA2[i]),str(A3[i]),str(errA3[i]),str(A4[i]),str(errA4[i])+"\n"])

# p, MJD, flux, errflux, Bin, TS, A1, errA1, A2, errA2, A3, errA3, A4, errA4 = np.loadtxt('/home/vital/Desktop/J14488_like_lc.dat', delimiter=' ',dtype=float, usecols=None, unpack=True)
# JD = MJD + 2400000.5 - 2450000.0
# 
# print MJD
# print JD

f = open('/home/vital/Desktop/TS25.txt', 'w')
g = open('/home/vital/Desktop/TS9.txt', 'w')
     
for i in range(len(JD)):
    if TS[i] >= 25:
        new_line = '{JD_entry} {flux_entry} {errflux_entry} {Bin_entry} {TS_entry} {A1_entry} {errA1_entry} {A2_entry} {errA2_entry} {A3_entry} {errA3_entry} {A4_entry} {errA4_entry}\n'.format(
        JD_entry=JD[i], flux_entry=flux[i], errflux_entry=errflux[i], Bin_entry=Bin[i], TS_entry=TS[i], A1_entry=A1[i], errA1_entry=errA1[i], A2_entry=A2[i], errA2_entry=errA2[i], A3_entry=A3[i], errA3_entry=errA3[i], A4_entry=A4[i], errA4_entry=errA4[i])   
        f.writelines(new_line)
    if TS[i] >= 9:
        new_line = ' '.format()
        new_line = '{JD_entry} {flux_entry} {errflux_entry} {Bin_entry} {TS_entry} {A1_entry} {errA1_entry} {A2_entry} {errA2_entry} {A3_entry} {errA3_entry} {A4_entry} {errA4_entry}\n'.format(
        JD_entry=JD[i], flux_entry=flux[i], errflux_entry=errflux[i], Bin_entry=Bin[i], TS_entry=TS[i], A1_entry=A1[i], errA1_entry=errA1[i], A2_entry=A2[i], errA2_entry=errA2[i], A3_entry=A3[i], errA3_entry=errA3[i], A4_entry=A4[i], errA4_entry=errA4[i])
        g.writelines(new_line)

f.close()
g.close()
        
