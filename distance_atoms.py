from math import sqrt

class Molecule:
    def __init__(self, path):
        self.f = open(path, 'r')
        self.datos = self.f.readlines()
        self.atom, self.x, self.y, self.z = [], [], [], []
        self.Z1, self.Z = 0, 0
        self.MPP_round, self.SPD_round = 0, 0
        self.xx1, self.yy1 = 0, 0
        self.a0, self.a1, self.a2, = 0, 0, 0

    def set_arrays(self):
        for i in range(len(self.datos)):
            coords = self.datos[i].split()
            self.atom.append(coords[0])
            self.x.append(float(coords[1]))
            self.y.append(float(coords[2]))
            self.z.append(float(coords[3]))
            self.f.close()
    def calculate_distance_atoms(self):
        distance = {}
        for i in range(len(self.x)):
            aux = []  
            for j in range(len(self.x)):
                aux.append(sqrt(pow((self.x[i-1]-self.x[j-1]), 2)+
                               pow((self.y[i-1]-self.y[j-1]), 2)+
                               pow((self.z[i-1]-self.z[j-1]), 2))) 
            distance["ATOM: "+str(i)] = aux  
        return distance    

mol = Molecule("y18-Cl-simplif-HSE-TD-6311G.xyz")
mol.set_arrays()
d= mol.calculate_distance_atoms()

for atom in d:
    print(atom ,"-->\n",d[atom])
print(mol.atom)