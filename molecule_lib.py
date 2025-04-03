import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from math import sqrt

COLOR_ATOMS = {"H": "#FFFFFF", "C": "#909090", "N": "#3050F8", "O": "#FF0D0D", "F": "#90E050",
               "Cl": "#1FF01F", "Br": "#A62929", "I": "#940094"}

def open_file_xyz(file_xyz):
    f = open(file_xyz, 'r')
    data = f.readlines()
    f.close()
    return data

class Atom:
    
    def __init__(self, element, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.element = element
        
    def distance_atom(self, Atom):
        distance = sqrt(pow((self.x-Atom.x), 2)+
                       pow((self.y-Atom.y), 2)+
                       pow((self.z-Atom.z), 2))
        return distance
    
    def set_color(self):
        value_color = COLOR_ATOMS
        if self.element in value_color:
            return value_color[self.element]
  
        
        
class Molecule:
    
    def __init__(self, xyz):
        self.xyz = xyz
        self.atoms = []
        self.set_arrays()
        
    def set_arrays(self):
        for i in range(len(self.xyz)):
            coordinate = self.xyz[i].split()
            self.atoms.append(Atom(coordinate[0], 
                             float(coordinate[1]), 
                             float(coordinate[2]), 
                             float(coordinate[3])))
     
    def calculate_links(self):
        atoms_links = set()
        
        for i in range(len(self.xyz)): 
            
            for j in range(len(self.xyz)): 
                
                distance = self.atoms[i].distance_atom(self.atoms[j]) 
                
                if((distance < 1.5 and distance > 1.3) and 
                  (self.atoms[i].element == self.atoms[j].element)and self.atoms[i].element == "C"  ):
                    print(distance)
                    link = "{}-{}".format(i,j) 
                    if (link not in atoms_links) and (link[::-1] not in atoms_links):
                        atoms_links.add(link)
        return atoms_links
     
    
    def graph(self):
        
        fig = plt.figure(figsize=(8, 8))
        ax = Axes3D(fig)
        atoms_links = self.calculate_links() 
        
        for i in range(len(self.atoms)):
            for j in range(len(self.atoms)):
                link = "{}-{}".format(i,j)
                x = [self.atoms[i].x, self.atoms[j].x]
                y = [self.atoms[i].y, self.atoms[j].y]
                z = [self.atoms[i].z, self.atoms[j].z]
                
                if link in atoms_links:
                    ax.plot3D(x,y,z,color="blue")
       
        
        #Atoms graphic
        for k in range(len(self.atoms)):
            ax.scatter(self.atoms[k].x, self.atoms[k].y, self.atoms[k].z, color=self.atoms[k].set_color())
            
        plt.show()
        
        




class MolecularPlanarity():
    
    def __init__(self, xyz):
        super().__init__(xyz)
        self.Z1, self.Z = 0, 0
        self.MPP_round, self.SPD_round = 0, 0
        self.a0, self.a1, self.a2, = 0, 0, 0
        self.element, self.x, self.y, self.z = [], [], [], []
    
    def set_arrays(self):
        for i in range(len(self.xyz)):
            coordinate = self.xyz[i].split()
            self.element.append(coordinate[0])
            self.x.append(float(coordinate[1]))
            self.y.append(float(coordinate[2]))
            self.z.append(float(coordinate[3]))
        
        
    def calculate_ds(self):
        xdata = np.column_stack((self.x, self.y))
        reg = linear_model.LinearRegression().fit(xdata, self.z)
        self.a0 = reg.intercept_
        self.a1, self.a2 = reg.coef_
        d = []
        for i in range(len(self.x)):
            di = (self.a0+self.a1*self.x[i]+self.a2*self.y[i]-self.z[i])/((self.a1**2+self.a2**2+1)**0.5)
            d.append(di)
    
        d2 = []
        for j in range(len(d)):
            d2.append(d[j]**2)
    
        mpp = np.sqrt((1/len(self.x))*sum(d2))
        self.MPP_round = round(mpp, 5)
        self.SPD_round = round(max(d)-min(d), 5)    
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        