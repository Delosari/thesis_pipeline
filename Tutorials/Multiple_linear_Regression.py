# import numpy as np
# import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d.axes3d as axes3d
# 
# fig = plt.figure(dpi=100)
# ax = fig.add_subplot(111, projection='3d')
# 
# #data
# fx = [0.673574075,0.727952994,0.6746285]
# fy = [0.331657721,0.447817839,0.37733386]
# fz = [18.13629648,8.620699842,9.807536512]
# 
# #error data
# xerror = [0.041504064,0.02402152,0.059383144]
# yerror = [0.015649804,0.12643117,0.068676131]
# zerror = [3.677693713,1.345712547,0.724095592]
# 
# #plot points
# ax.plot(fx, fy, fz, linestyle="None", marker="o")
# 
# #plot errorbars
# for i in np.arange(0, len(fx)):
#     ax.plot([fx[i]+xerror[i], fx[i]-xerror[i]], [fy[i], fy[i]], [fz[i], fz[i]], marker="_")
#     ax.plot([fx[i], fx[i]], [fy[i]+yerror[i], fy[i]-yerror[i]], [fz[i], fz[i]], marker="_")
#     ax.plot([fx[i], fx[i]], [fy[i], fy[i]], [fz[i]+zerror[i], fz[i]-zerror[i]], marker="_")
# 
# #configure axes
# ax.set_xlim3d(0.55, 0.8)
# ax.set_ylim3d(0.2, 0.5)
# ax.set_zlim3d(8, 19)
# 
# plt.show()

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#data
fname = ["acb","fgj","asd","tert","hjk","aer","cvb","ghj","qwf","hng","cde","iolk","xsa","ong","aasd","ghgh","rtrt","wewe","qwqw","bnbn","jhgd","aghty","dfg","derA","eryh","asdq","Dbgd","SsadI"]
fx = [0.673574075,0.727952994,0.6745,0.793558,0.37664721,0.67939197,0.748490102,0.722048276,0.767189284,0.768296082,0.732383162,0.748429373,0.751570337,0.698977802,0.703398777,0.802607746,0.786242535,0.366661714,0.792490268,0.698636545,0.769904493,0.762656928,0.478595152,0.759151743,0.728607906,0.778099194,0.728575153,0.703794547]
fy = [0.21,0.49,0.36,0.304,0.1009,0.329287287,0.752,0.309,0.277462605,0.333935925,0.326699919,0.72242944,0.358848707,0.298222369,0.03486,0.43058538,0.373973649,0.12288,0.9444,0.2494,0.384761779,0.382446444,0.35914706,0.298360515,0.391041147,0.363895412,0.312359532,0.343344197]
fz = [18,8.620699842,9.2,17.40183,24.44101897,18,8.075948931,19,22.24192367,15,13.28436202,4.472128831,14.53195939,15.93922217,0,0,11.28194885,0,0,26.12423918,9.200498046,14.01392223,14.14545413,17.8320704,8.985897324,10.53443457,12.48561226,11.80438073]

#errorbar data
xSD = [0.041504064,0.02402152,0.059383144,0.038393713,0.054242278,0.018450667,0.083524242,0.042438697,0.036334793,0.023742101,0.041280224,0.003936522,0.025525758,0.031090602,0.027155833,0.038639074,0.061699064,0.11610088,0.075548578,0.059801071,0.069031082,0.071645685,0.050143938,0.049165738,0.020437116,0.046606225,0.039779165,0.019699934]
ySD = [0.015649804,0.12643117,0.068676131,0.016337,0.015050422,0.0651138,0,0.028590823,0.033705502,0.025962039,0,0,0.036646619,0.062000616,0,0,0.026584944,0.005923891,0,0.027485812,0,0.058142106,0.004978857,0.011233057,0.051596586,0.013837766,0,0.054340381]
zSD = [3.677693713,1.345712547,0.724095592,1.856309389,34.56482051,1.487978871,0,1.173906828,2.887602472,0.305603391,0,0,1.791653266,3.842020113,0,0,0.474818671,0,0,5.113750225,0,1.113374167,0.264111881,2.483847286,2.787214029,0.60047479,0,3.881040381]


#Class for 3d object
class thriidii:
    def __init__ (self, azimuut, elevation, x, y, z, d, n, gr, oy, oz, axesS, xl, yl, zl, prj, COL, randinp):
        
        
        self.AZ = azimuut 
        self.EL = elevation
    
        self.Dx = x
        self.Dy = y
        self.Dz = z
        
        #get limits
        
        self.maxDx = np.max(self.Dx)
        self.maxDy = np.max(self.Dy)
        self.maxDz = np.max(self.Dz)
        
        self.minDx = np.min(self.Dx)
        self.minDy = np.min(self.Dy)
        self.minDz= np.min(self.Dz)
        
        self.maxXYZ = np.max([np.max(self.Dx), np.max(self.Dy), np.max(self.Dz)])
        self.minXYZ = np.min([np.min(self.Dx), np.min(self.Dy), np.min(self.Dz)])        
        
        self.maxXY = np.max([np.max(self.Dx), np.max(self.Dy)])
        self.minXY = np.min([np.min(self.Dx), np.min(self.Dy)])        
        
        self.maxXZ = np.max([np.max(self.Dx), np.max(self.Dz)])
        self.minXZ = np.min([np.min(self.Dx), np.min(self.Dz)])        
        
        self.maxYZ = np.max([np.max(self.Dy), np.max(self.Dz)])
        self.minYZ = np.min([np.min(self.Dy), np.min(self.Dz)])
        
        print "MAX Dx", self.maxDx
        print "MAX Dy", self.maxDy 
        print "MAX Dz", self.maxDz
        
        print "MIN Dx", self.minDx 
        print "MIN Dy", self.minDy
        print "MIN Dz", self.minDz
        
        
        
        
        
        for i in  np.arange(0, len(self.Dx)):
            
            #plot data points
            ax.plot([self.Dx[i]], [self.Dy[i]], [self.Dz[i]], ls="None", marker=".", zorder=90, color=COL, mec=COL)
            #plot 3d errorbars 
            ax.plot([self.Dx[i]-xSD[i], self.Dx[i]+xSD[i]], [self.Dy[i], self.Dy[i]], [self.Dz[i], self.Dz[i]], alpha=0.3, ls="-", marker="_", zorder=90, color=COL, mec=COL)
            ax.plot([self.Dx[i], self.Dx[i]], [self.Dy[i]-ySD[i], self.Dy[i]+ySD[i]], [self.Dz[i], self.Dz[i]], alpha=0.3, ls="-", marker="_", zorder=90, color=COL, mec=COL) 
            ax.plot([self.Dx[i], self.Dx[i]], [self.Dy[i], self.Dy[i]], [self.Dz[i]-zSD[i], self.Dz[i]+zSD[i]], alpha=0.3, ls="-", marker="_", zorder=90, color=COL, mec=COL) 
            
            
        #if gr = 1, plot names next to data
        if gr == 1:
            for i in np.arange(0, len(self.Dx)):
                ax.text(self.Dx[i], self.Dy[i]+oy, self.Dz[i]+oz,  "%s" % (n[i]), size=10, color=COL, zorder=100)
               
        else:
            print gr
        

        #function to plot projections (2d plots)    
        def tuudii(arname, asim, elev, axesss): 
            for j in set(arname): #iterate trough unique elements in name list
                
                iii = -1
                temp_array = []
                try:
                    while 1:
                        
                        iii = arname.index(j, iii+1) #find all maching indexes for names
                        print "match at", iii, j
                        temp_array.append(iii)
                        #ax.plot([self.Dx[i]], [self.Dy[i]], [self.minDz], ms="x", color="red", zorder=200)
                        
                            
                    
                except ValueError:
                    tmp_2dx = []
                    tmp_2dy = []
                    tmp_2dz = []
                    
                    tmp_2dx_cont = []                  
                    tmp_2dy_cont = []
                    tmp_2dz_cont = []
                    
                    if axesss == 3:
                        minX = self.minXYZ
                        minY = self.minXYZ
                        minZ =self.minXYZ
                        maxX =self.maxXYZ
                        maxY =self.maxXYZ
                        maxZ =self.maxXYZ
                    if axesss == 2:
                        minX = self.minXY
                        minY = self.minXY
                        minZ =self.minDz
                        maxX =self.maxXY
                        maxY =self.maxXY
                        maxZ =self.maxDz                
                    if axesss == 1:
                        minX = self.minXZ
                        minY = self.minDy
                        minZ =self.minXZ
                        maxX =self.maxXZ
                        maxY =self.maxDy
                        maxZ =self.maxXZ
                        
                    if axesss == 0:
                        minX = self.minDx
                        minY = self.minYZ
                        minZ =self.minYZ
                        maxX =self.maxDx
                        maxY =self.maxYZ
                        maxZ =self.maxYZ
                    if axesss == 4:
                        minX = self.minDx
                        minY = self.minDy
                        minZ =self.minDz
                        maxX =self.maxDx
                        maxY =self.maxDy
                        maxZ =self.maxDz
                    else:
                        pass
                        
                    for i in temp_array:
                    
                        tmp_2dx.append(self.Dx[i])
                        tmp_2dy.append(self.Dy[i])
                        tmp_2dz.append(self.Dz[i])
                        #depending of plotting angle choose where to plot projections
                        if asim < 90:
                            tmp_2dx_cont.append(minX)
                            x_cont = minX
                            tmp_2dy_cont.append(minY)
                            y_cont = minY
                        else:
                            tmp_2dx_cont.append(maxX)
                            x_cont = maxX
                            tmp_2dy_cont.append(minY)
                            y_cont = minY
                        
                        if elev > 0:
                            tmp_2dz_cont.append(minZ)
                            z_cont = minZ
                        else:
                            tmp_2dz_cont.append(maxZ)
                            z_cont = maxZ

                        
                    ax.plot(tmp_2dx, tmp_2dy, tmp_2dz_cont, ls="dotted", color="#C0C0C0")
                    
                    
                    ax.plot(tmp_2dx, tmp_2dy_cont, tmp_2dz, ls="dotted", color="#C0C0C0")
                    
                    
                    ax.plot(tmp_2dx_cont, tmp_2dy, tmp_2dz, ls="dotted", color="#C0C0C0")
                    
                    
                    
                    for k in temp_array:
                        print "K:", k
                        ax.plot([x[k]], [y[k]], [z_cont], marker=".", color="#C0C0C0")
                        
                        ax.plot([x[k]-xSD[k], x[k]+xSD[k]], [y[k], y[k]], [z_cont, z_cont], alpha=0.3,marker="_", color="#C0C0C0")
                        ax.plot([x[k], x[k]], [y[k]-ySD[k], y[k]+ySD[k]], [z_cont, z_cont], alpha=0.3,marker="_", color="#C0C0C0")
                        
                        
                        
                        
                        ax.plot([x[k]], [y_cont], [z[k]], marker=".", color="#C0C0C0")
                        ax.plot([x[k]-xSD[k], x[k]+xSD[k]], [y_cont, y_cont], [z[k], z[k]], marker="_", color="#C0C0C0")
                        ax.plot([x[k], x[k]], [y_cont, y_cont], [z[k]-zSD[k], z[k]+zSD[k]], marker="_", color="#C0C0C0")
                        
                                         
                        
                        ax.plot([x_cont], [y[k]], [z[k]], marker=".", color="#C0C0C0")
                        
                        ax.plot([x_cont, x_cont], [y[k]-ySD[k], y[k]+ySD[k]], [z[k], z[k]], marker="_", color="#C0C0C0")
                        ax.plot([x_cont, x_cont], [y[k], y[k]], [z[k]-zSD[k], z[k]+zSD[k]], marker="_", color="#C0C0C0")
                        
                        
                        
                        ax.text(self.Dx[k], self.Dy[k]+0.01, z_cont+0.5,  "%s" % (n[k]), size=9, zorder=1, color="#C0C0C0")
                        ax.text(self.Dx[k], y_cont+0.01, self.Dz[k]+0.5,  "%s" % (n[k]), size=9, zorder=1, color="#C0C0C0")
                        ax.text(x_cont, self.Dy[k]+0.01, self.Dz[k]+0.5,  "%s" % (n[k]), size=9, zorder=1, color="#C0C0C0")
                        
                        
                        
        
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
        ax.set_zlabel(zl)
        
        #uncomment next 2 lines to draw a viewing angle information on the plot
        
        #TITLE = "az: %s, el: %s" % (self.AZ, self.EL)
        #plt.title(TITLE)
            
        ax.azim = self.AZ
        ax.elev = self.EL
        


            
            
        if prj == 1:
            tuudii(n, self.AZ, self.EL, axesS)
            
            
        else:
            pass
        
        
        if axesS == 4:
            ax.set_xlim3d(self.minDx,self.maxDx)
            ax.set_ylim3d(self.minDy,self.maxDy)
            ax.set_zlim3d(self.minDz,self.maxDz)
            print "XYZ min:",self.minXYZ,"XYZ max:",self.maxXYZ
        if axesS == 3:
            ax.set_xlim3d(self.minXYZ,self.maxXYZ)
            ax.set_ylim3d(self.minXYZ,self.maxXYZ)
            ax.set_zlim3d(self.minXYZ,self.maxXYZ)
            print "XYZ min:",self.minXYZ,"XYZ max:",self.maxXYZ
        if axesS == 2:
            ax.set_xlim3d(self.minXY,self.maxXY)
            ax.set_ylim3d(self.minXY,self.maxXY)
            ax.set_zlim3d(self.minDz,self.maxDz)
            print "XY min:",self.minXYZ,"XY max:",self.maxXYZ, "Z min:", self.minDz,"Z max:", self.maxDz        
        if axesS == 1:
            ax.set_xlim3d(self.minXZ,self.maxXZ)
            ax.set_ylim3d(self.minDy,self.maxDy)
            ax.set_zlim3d(self.minXZ,self.maxXZ)
            print "XZ min:",self.minXZ,"XZmax:",self.maxXZ, "Y min:", self.minDy,"Y max:", self.maxDy 
        if axesS == 0:
            ax.set_xlim3d(self.minDx,self.maxDx)
            ax.set_ylim3d(self.minYZ,self.maxYZ)
            ax.set_zlim3d(self.minYZ,self.maxYZ)
            print "YZ min:",self.minYZ,"YZmax:",self.maxYZ, "X min:", self.minDx,"X max:", self.maxDx
        else:
            pass
        #plt.savefig("%s.png" % (randinp), format="png")
        plt.show()
        
# azimuut, elevation, x, y, z, ,name_list, gr, norm, Ylabeloffset, Zlabeloffset, xlabel, ylabel, zlabel, projections, color, random number)

#with projections
#thriidii(45, 22, fx, fy, fz, fz, fname, 1,0.01, 0.5, 4, "speed", "might", "fame", 1, "green",1)

#without projections
thriidii(45, 22, fx, fy, fz, fz, fname, 1,0.01, 0.5, 4, "speed", "might", "fame", 0, "green",1)
