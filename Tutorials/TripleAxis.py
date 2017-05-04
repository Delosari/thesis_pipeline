#!/usr/bin/python

import sys
import pylab
import math
import numpy as np
import Vitools as vit
import matplotlib.pyplot as plt

ArgumentsCheck, Arguments = vit.Arguments_Checker(sys.argv)

print "Initiating " + Arguments[0][Arguments[0].rfind("/")+1:len(Arguments[0])] + " task\n"

FilesList, Flags = vit.Arguments_Handler(ArgumentsCheck, Arguments)

if ArgumentsCheck == False:  
    Folder = "/media/vital/Data/OBS-DATA/"  
    #Folder = "/home/vital/Desktop/Programing_Tests/"
    FilesList = vit.FilesFinder(Folder,"EBV_LinesLogv7_combined.txt")
    Flags = ["-0000","-1111"]

#-----------------------------------------------------------------------------------------------------

Fig1=plt.figure(figsize=(16,10))
AxHor0 = Fig1.add_subplot(111)

DataFolder = "/home/vital/Dropbox/Astrophysics/Data/HII_Galaxies/"

Objects = []
Y_Abundances = []
O_Abundances = []
N_Abundances = []
S_Abundances = []

FilesList.sort()

print "Files meeting emission lines requirements:"

for File in FilesList:
    ObjName, FileName, FolderName = vit.AddressAnalyzer(File)
    CodeName = ObjName[3:len(ObjName)]
    
    #Test = vit.GetDataInTable("Line_Label", "FluxGauss", "XXXXX", File, 2)

    OIII_4959_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "O3_4959A", File, 2)
    OIII_5007_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "O3_5007A", File, 2)
    OIII_4363_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "O3_4363A", File, 2)
    SII_6716_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "S2_6716A", File, 2)
    SII_6730_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "S2_6731A", File, 2)
    OII_7320_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "O2_7319A", File, 2)
    HBeta_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "H1_4861A", File, 2)
    NII_6548_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "N2_6548A", File, 2)
    NII_6583_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "N2_6584A", File, 2)
    HeI_4471_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "He1_4472A", File, 2)
    HeI_5876_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "He1_5876A", File, 2)
    HeI_6678_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "He1_6678A", File, 2)
    HeII_4686_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "He2_4686A", File, 2)
    SIII_9069_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "S3_9069A", File, 2)
    SIII_9534_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "S3_9531A", File, 2)
    SIII_6312_Flux = vit.GetDataInTable("Line_Label", "FluxGauss", "S3_6312A", File, 2)
    
    if (OIII_4959_Flux != "None") and (OIII_5007_Flux != "None") and (OIII_4363_Flux != "None") and (SII_6716_Flux != "None") and (SII_6730_Flux != "None") and (OII_7320_Flux != "None") and (HBeta_Flux != "None") and (NII_6548_Flux != "None") and (NII_6583_Flux != "None") and (HeI_4471_Flux != "None") and (HeI_5876_Flux != "None") and (HeI_6678_Flux != "None") and (HeII_4686_Flux != "None") and (SIII_9069_Flux != "None") and (SIII_9534_Flux != "None") and (SIII_6312_Flux != "None"):
        print "Obj " + CodeName
        if CodeName != "SHOC593" and CodeName != "SHOC579":
                       
            
            Objects.append(CodeName)
        
            OIII_4959_Flux = float(OIII_4959_Flux)
            OIII_5007_Flux = float(OIII_5007_Flux)
            OIII_4363_Flux = float(OIII_4363_Flux)
            SII_6716_Flux = float(SII_6716_Flux)
            SII_6730_Flux = float(SII_6730_Flux)
            OII_7320_Flux = float(OII_7320_Flux)
            HBeta_Flux = float(HBeta_Flux)
            NII_6548_Flux = float(NII_6548_Flux)
            NII_6583_Flux = float(NII_6583_Flux)
            HeI_4471_Flux = float(HeI_4471_Flux)
            HeI_5876_Flux = float(HeI_5876_Flux)
            HeI_6678_Flux = float(HeI_6678_Flux)
            HeII_4686_Flux = float(HeII_4686_Flux)
            SIII_9069_Flux = float(SIII_9069_Flux)
            SIII_9534_Flux = float(SIII_9534_Flux)
            SIII_6312_Flux = float(SIII_6312_Flux)
            
            
            ROIII = (OIII_4959_Flux + OIII_5007_Flux) / OIII_4363_Flux
            #Outfile.writelines('ROIII'+" "+str(ROIII)+'\n')
            #print OIII_4363_Flux
            
            T_OIII = 0.8254 - 0.0002415*ROIII + (47.77/ROIII)
            #Outfile.writelines('T_OIII'+" "+str(T_OIII)+'\n')
            
            RSII = SII_6716_Flux / SII_6730_Flux
            #Outfile.writelines('RSII'+" "+str(RSII)+'\n')
        
            a_0 = 2.21 - 1.3/T_OIII - 1.25*T_OIII + 0.23*T_OIII**2
            a_1 = -3.35 + 1.94/T_OIII + 1.93*T_OIII - 0.36*T_OIII**2
            b_0 = -4.33 + 2.33/T_OIII + 2.72*T_OIII - 0.57*T_OIII**2
            b_1 = 1.84 - 1.0/T_OIII - 1.14*T_OIII + 0.24*T_OIII**2
            
            n_SII = (10.0**3)*(RSII*a_0 + a_1)/(RSII*b_0 + b_1)
            #Outfile.writelines('n_SII'+" "+str(n_SII)+'\n')
        
            T_OII = (1.2 + 0.002*n_SII + 4.2/n_SII)/(1/T_OIII + 0.08 + 0.003*n_SII + 2.5/n_SII)
            #Outfile.writelines('T_OII'+" "+str(T_OII)+'\n')
        
            logOII_logHII = -12 + math.log10(OII_7320_Flux/HBeta_Flux) + 6.895 + 2.44/T_OII -0.58*math.log10(T_OII) - math.log10(1.0 + 0.0047*n_SII)
        
            logOIII_logHII = -12 + math.log10((OIII_4959_Flux+OIII_5007_Flux)/HBeta_Flux) + 6.144 + 1.251/T_OIII - 0.55*math.log10(T_OII)
        
            logNII_logHII = -12 + math.log10((NII_6548_Flux+NII_6583_Flux)/HBeta_Flux) + 6.273 + 0.894/T_OII - 0.592*math.log10(T_OII)
            
            OII_HII = 10**(logOII_logHII)
            #Outfile.writelines('OII_HII'+" "+str(OII_HII)+'\n')
            
            OIII_HII = 10**(logOIII_logHII)
            #Outfile.writelines('OIII_HII'+" "+str(OIII_HII)+'\n')
            
            NII_HII = 10**(logNII_logHII)
            #Outfile.writelines('NII_HII'+" "+str(NII_HII)+'\n')
            
            NI_OI = (NII_HII)/(OII_HII) 
            #Outfile.writelines('NI_OI'+" "+str(NI_OI)+'\n')
            
            OI_HI = OII_HII + OIII_HII
            #Outfile.writelines('OI_HI'+" "+str(OI_HI)+'\n')
            O_Abundances.append(OI_HI)
            
            NI_HI = NI_OI * OI_HI
            N_Abundances.append(NI_HI)
            #Outfile.writelines('NI_HI'+" "+str(NI_HI)+'\n')
            
            #print HeI_4471_Flux,HBeta_Flux,T_OIII
            y0_I4471 = 2.04 * (T_OIII**0.13) * HeI_4471_Flux / HBeta_Flux
            y0_I5876 = 0.783 * (T_OIII**0.23) * HeI_5876_Flux / HBeta_Flux
            y0_I6678 = 2.58 * (T_OIII**0.25) * HeI_6678_Flux / HBeta_Flux
            y_PPI4686 = 0.084 * (T_OIII**0.14) * HeII_4686_Flux / HBeta_Flux
        
            D = 1.0 + 3110.0*(T_OIII**-0.51)*(1.0/n_SII)
            g_I4471 = 6.11 * (T_OIII**0.02) * (math.e**-4.544) / D
            g_I5876 = (7.12 * (T_OIII**0.14) * (math.e**(-3.776/T_OIII)) + 1.47 * (T_OIII**-0.28) * (math.e**(-4.544/T_OIII)))/ D
            g_I6678 = (3.27 * (T_OIII**-0.41) * (math.e**(-3.777/T_OIII)) + 0.49 * (T_OIII**-0.52) * (math.e**(-4.544/T_OIII)))/ D
            
            y_I4471 = y0_I4471/(1.0 + g_I4471)
            y_I5876 = y0_I5876/(1.0 + g_I5876)
            y_I6678 = y0_I6678/(1.0 + g_I6678)
            
            HeII_HII = (0.6)*(y_I5876 + (0.333333)*y_I4471 + (0.333333)*y_I6678)
            #Outfile.writelines('HeII_HII'+" "+str(HeII_HII)+'\n')
            
            HeIII_HII = y_PPI4686
            #Outfile.writelines('HeIII_HII'+" "+str(HeIII_HII)+'\n')
            
            He_H = HeII_HII + HeIII_HII
            #Outfile.writelines('He_H'+" "+str(He_H)+'\n')
            
            Y = (4.0 * He_H*(1.0 - 20.0 * OI_HI)) / (1.0 + 4.0 * He_H)
            #Outfile.writelines('Y'+" "+str(Y)+'\n')
            Y_Abundances.append(Y)
            
            R_SIII = (SIII_9069_Flux + SIII_9534_Flux) / SIII_6312_Flux
            #Outfile.writelines('R_SIII'+" "+str(R_SIII)+'\n')
            
            T_SIII = (R_SIII + 36.4) / (1.8*R_SIII - 3.01)
            
            logSII_logHII = -12+ math.log10((SII_6716_Flux + SII_6730_Flux) / HBeta_Flux) + 5.423 + 0.929/T_SIII - 0.28 * math.log10(T_SIII)
            
            logSIII_logHII = -12 + math.log10((SIII_9069_Flux + SIII_9534_Flux) / HBeta_Flux) + 5.8 + 0.771/T_SIII - 0.28 * math.log10(T_SIII)
            
            SII_HII = 10**logSII_logHII
            #Outfile.writelines('SII_HII'+" "+str(SII_HII)+'\n')
            
            SIII_HII = 10**logSIII_logHII
            #Outfile.writelines('SIII_HII'+" "+str(SIII_HII)+'\n')
            
            S_O = (SII_HII + SIII_HII)/(OII_HII + OIII_HII)
            #Outfile.writelines('S_O'+" "+str(S_O)+'\n')
            
            S_H = S_O * OI_HI
            #Outfile.writelines('S_H'+" "+str(S_H)+'\n')
            S_Abundances.append(S_H)
    
vit.GenerateOneFrameFigure("Linear Regresion Primordial Helium", "O/H","Y", Fig1, AxHor0)
 
#plt.axhline(y=2.86, xmin=0, xmax=1,color = "r",linestyle = "--") #Dashed line representing median continuum
print Objects
print O_Abundances
print S_Abundances
print N_Abundances
print Y_Abundances



AxHor1 = AxHor0.twiny()
AxHor2 = AxHor1.twiny()
Fig1.subplots_adjust(bottom=0.20)

AxHor0.set_xlabel("Oxygen")
AxHor1.set_xlabel("Nitrogen")
AxHor2.set_xlabel("Sulphur")
AxHor0.legend()


AxHor1.set_frame_on(True)
AxHor1.patch.set_visible(False)
AxHor1.xaxis.set_ticks_position('bottom')
AxHor1.xaxis.set_label_position('bottom')
AxHor1.spines['bottom'].set_position(('outward', 45))

AxHor2.set_frame_on(True)
AxHor2.patch.set_visible(False)
AxHor2.xaxis.set_ticks_position('bottom')
AxHor2.xaxis.set_label_position('bottom')
AxHor2.spines['bottom'].set_position(('outward', 90))

AxHor0.plot(O_Abundances,Y_Abundances, "o", color="green", label="Oxygen")
AxHor1.plot(N_Abundances, Y_Abundances, "*", color="blue", label = "Nitrogen")
AxHor2.plot(S_Abundances, Y_Abundances,'>', color="orange", label = "Sulphur")

AxHor0.legend(bbox_to_anchor=(0.95,0.95))
AxHor1.legend(bbox_to_anchor=(0.95,0.90))
AxHor2.legend(bbox_to_anchor=(0.95,0.85))

AxHor0.set_xlabel('Oxygen')
AxHor1.set_xlabel('Nitrogen')
AxHor2.set_xlabel('Sulphur')

AxHor0.set_ylim(0.10, 0.35)
AxHor0.set_xlim(0, max(O_Abundances)*1.10)
AxHor1.set_xlim(0, max(N_Abundances)*1.10)
AxHor2.set_xlim(0, max(S_Abundances)*1.10)

x0_np = np.array(O_Abundances)
x1_np = np.array(N_Abundances)
x2_np = np.array(S_Abundances)

y_np = np.array(Y_Abundances)
# 
A0 = np.vstack([x0_np, np.ones(len(x0_np))]).T
m0, n0 = np.linalg.lstsq(A0, y_np)[0]

A1 = np.vstack([x1_np, np.ones(len(x1_np))]).T
m1, n1 = np.linalg.lstsq(A1, y_np)[0]

A2 = np.vstack([x2_np, np.ones(len(x2_np))]).T
m2, n2 = np.linalg.lstsq(A2, y_np)[0]
#
TrendX = np.array([0,1]) 
TrendLine0 =  AxHor0.plot(TrendX, m0*TrendX+n0, '--', color="green")
TrendLine1 =  AxHor1.plot(TrendX, m1*TrendX+n1, '--', color="blue")
TrendLine0 =  AxHor2.plot(TrendX, m2*TrendX+n2, '--', color="orange")

#Axis1.plot(0.0,24,"o",color="r")
"/media/vital/Data/LinearRegresion.pdf"
plt.savefig("/media/vital/Data/LinearRegresion.pdf", dpi=600)

print "Primordial value:"
#print n

plt.show()

#-----------------------------------------------------------------------------------------------------

print "\nEnding: " + Arguments[0][Arguments[0].rfind("/")+1:len(Arguments[0])] + " task\n"