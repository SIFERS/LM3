import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Molecule:
    def __init__(self,path):
        self.path = path
        self.f=open(path,'r')
        self.datos =self.f.readlines()
        self.atom,self.x,self.y,self.z = [],[],[], []
    
    def set_arrays(self):
        for i in range(len(self.datos)):
            self.coords = self.datos[i].split()
            self.atom.append(self.coords[0])
            self.x.append(float(self.coords[1]))
            self.y.append(float(self.coords[2]))
            self.z.append(float(self.coords[3]))
            self.f.close()
           
    
    def plane_adjustment(self):
        self.Xdata = np.column_stack((self.x, self.y))
        from sklearn import linear_model
        self.reg = linear_model.LinearRegression().fit(self.Xdata, self.z)
        self.a0=self.reg.intercept_
        self.a1, self.a2 = self.reg.coef_


        self.maya_x=np.linspace(min(self.x),max(self.x),10)
        self.maya_y=np.linspace(min(self.y),max(self.y),10)

        self.xx1, self.yy1 = np.meshgrid(self.maya_x,self.maya_y)

        self.xx,self.yy = np.meshgrid(self.x,self.y)

        self.Z = self.a0+self.a1*self.xx+self.a2*self.yy
        self.Z1= self.a0+self.a1*self.xx1+self.a2*self.yy1    
       

    def calculate_ds(self):
        self.d = []
        for i in range(len(self.x)):
            self.di = (self.a0+self.a1*self.x[i]+self.a2*self.y[i]-self.z[i])/((self.a1**2+self.a2**2+1)**(0.5))
            self.d.append(self.di)

        self.d2= []
        for j in range(len(self.d)):
            self.d2.append(self.d[j]**2)
        

        self.MPP= np.sqrt((1/len(self.x))*sum(self.d2))
        self.MPP_round=round(self.MPP,5)
        self.SPD_round=round(max(self.d)-min(self.d),5)
  
    
    def graph(self):
        
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111, projection='3d')

        def set_color(_atom,index):
            value_color= dict
            value_color = {"H":"#FFFFFF","C":"#909090","N":"#3050F8","O":"#FF0D0D","F":"#90E050","Cl":"#1FF01F","Br":"#A62929","I":"#940094"}
            if(_atom[index] in value_color):
                return value_color[_atom[index]]
        
        ax.plot_wireframe(self.xx1, self.yy1, self.Z1, color='b', alpha=0.3)
        for k in range(len(self.x)):

            COLOR= set_color(self.atom,k)

            ax.scatter(self.x[k],self.y[k],self.z[k],color =COLOR) # plot the point (2,3,4) on the figure
        plt.show()
       
    def execute(self):
        self.set_arrays()
        self.plane_adjustment()
        self.calculate_ds()
        self.graph()



molecula1 = Molecule("y18-Cl-simplif-HSE-TD-6311G.xyz") 
molecula1.execute()
