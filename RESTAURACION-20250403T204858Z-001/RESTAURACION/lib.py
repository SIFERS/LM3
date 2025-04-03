import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from math import sqrt
from os.path import splitext


COLOR_ATOMS = {"H": "#FFFFFF", "C": "#909090", "N": "#3050F8", "O": "#FF0D0D", "F": "#90E050",
               "Cl": "#1FF01F", "Br": "#A62929", "I": "#940094", "S": "#FFFF30"}

elements = {
    1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B',
    6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne',
    11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P',
    16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca',
    21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn',
    26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn',
    31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br',
    36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr',
    41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh',
    46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn',
    51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs',
    56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd',
    61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb',
    66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb',
    71: 'Lu', 72: 'Hf', 73: 'Ta', 74: 'W', 75: 'Re',
    76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg',
    81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At',
    86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th',
    91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am',
    96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es', 100: 'Fm',
    101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db',
    106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds',
    111: 'Rg', 112: 'Cn', 113: 'Uut', 114: 'Fl', 115: 'Uup', 
    116: 'Lv', 117: 'Uus', 118: 'Uuo'}

def open_file(file):
    f = open(file, 'r')
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
        distance = sqrt(pow((self.x - Atom.x), 2) +
                        pow((self.y - Atom.y), 2) +
                        pow((self.z - Atom.z), 2))
        return distance

    def set_color(self):
        value_color = COLOR_ATOMS
        if self.element in value_color:
            return value_color[self.element]


class Molecule:

    def __init__(self, file):
        self.xyz = open_file(file)
        self.atoms = []
        self.set_arrays()

    def set_arrays(self):
        self.xyz.pop(0)
        self.xyz.pop(0)
        
        for i in range(len(self.xyz)):
            coordinate = self.xyz[i].split()
            self.atoms.append(Atom(coordinate[0],
                                   float(coordinate[1]),
                                   float(coordinate[2]),
                                   float(coordinate[3])))

    def calculate_links(self):
        atoms_links = set()
        
        def set_atoms(head, tail, a1, a2):
            if ((head > distance > tail) and
                    (self.atoms[i].element == a1 and self.atoms[j].element == a2)):
                link = "{}-{}".format(i, j)
                if (link not in atoms_links) and (link[::-1] not in atoms_links):
                    atoms_links.add(link)
           
        for i in range(len(self.xyz)):

            for j in range(len(self.xyz)):

                distance = self.atoms[i].distance_atom(self.atoms[j])

                set_atoms(1.54, 1.2, "C", "C")
                set_atoms(1.12, 1.06, "C", "H")
                set_atoms(2, 1, "C", "N")
                set_atoms(1.8, 1.7, "C", "Cl")
                set_atoms(1.8, 1.7, "C", "S")
                set_atoms(1.6, 1.2, "C", "O")
                set_atoms(1.5, 1.2, "N", "N")
                set_atoms(1.5, 1.2, "C", "F")
                set_atoms(1.9, 1.7, "C", "Br")
           

        return atoms_links

    def graph(self):

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(projection='3d')
        ax.set_facecolor('#000000')
       
        atoms_links = self.calculate_links()

        for i in range(len(self.atoms)):
            for j in range(len(self.atoms)):
                link = "{}-{}".format(i, j)
                x = [self.atoms[i].x, self.atoms[j].x]
                y = [self.atoms[i].y, self.atoms[j].y]
                z = [self.atoms[i].z, self.atoms[j].z]

                if link in atoms_links:
                    ax.plot3D(x, y, z, color="b")

        # Atoms graphic
        for k in range(len(self.atoms)):
            ax.scatter(self.atoms[k].x, self.atoms[k].y, self.atoms[k].z, color=self.atoms[k].set_color(), s=50)
        plt.axis("off")
        plt.savefig("figura_base.jpg")
        plt.savefig("figura_300dpi.jpg", dpi=300)
        plt.savefig("figura_600dpi.jpg", dpi=600)
        plt.show()
    def graph_GUI(self):
    
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(projection='3d')
        ax.set_facecolor('#000000')
       
        atoms_links = self.calculate_links()
    
        for i in range(len(self.atoms)):
            for j in range(len(self.atoms)):
                link = "{}-{}".format(i, j)
                x = [self.atoms[i].x, self.atoms[j].x]
                y = [self.atoms[i].y, self.atoms[j].y]
                z = [self.atoms[i].z, self.atoms[j].z]
    
                if link in atoms_links:
                    ax.plot3D(x, y, z, color="b")
    
        # Atoms graphic
        for k in range(len(self.atoms)):
            ax.scatter(self.atoms[k].x, self.atoms[k].y, self.atoms[k].z, color=self.atoms[k].set_color(), s=50)
        plt.axis("off")
        return plt


class MolecularPlanarity():

    def __init__(self, file):
        self.xyz = open_file(file)
        self.Z1, self.Z = 0, 0
        self.MPP_round, self.SPD_round = 0, 0
        self.a0, self.a1, self.a2, = 0, 0, 0
        self.element, self.x, self.y, self.z = [], [], [], []

    def set_arrays(self):
        self.xyz.pop(0)
        self.xyz.pop(0)
        
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
            di = (self.a0 + self.a1 * self.x[i] + self.a2 * self.y[i] - self.z[i]) / (
                    (self.a1 ** 2 + self.a2 ** 2 + 1) ** 0.5)
            d.append(di)

        d2 = []
        for j in range(len(d)):
            d2.append(d[j] ** 2)

        mpp = np.sqrt((1 / len(self.x)) * sum(d2))
        self.MPP_round = round(mpp, 3)
        self.SPD_round = round(max(d) - min(d), 3)
        
    def planarity(self):
        self.set_arrays()
        self.calculate_ds()
        
        
        
class damGen():
    
    
    
    
    def __init__(self, accep, donor, labels):
        self.accep = accep
        self.donor = donor
        self.labels = labels
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["New Century Schoolbook"]})


        xmin = min(self.accep)-0.2
        xmax = max(self.accep)+0.2
        ymin = min(self.donor)-0.2
        ymax = max(self.donor)+0.2
        markers=["o","v","^","<",">","s","p","P","*","X","1","2","3","4"]

        for i in range(len(self.accep)):
            plt.scatter(self.accep[i], self.donor[i], label=labels[i],marker=markers[i])

        plt.axhline(y = (ymin+ymax)/2, color = 'k', linestyle = '--' )
        plt.axvline(x = (xmin+xmax)/2, color = 'k', linestyle = '--' )

        plt.xlabel(r'$\omega^+$ (eV)',size=20)
        plt.ylabel(r'$\omega^-$ (eV)',size=20)

        plt.legend(bbox_to_anchor=(1.35, 1))
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)
        plt.grid()
        
    def show():
        plt.show()
        
class log2():
    
    def __init__(self, file):
        self.file= file 
        self.file_type = None
        
    def convert(self, file_type):
        self.file_type = file_type
        fly_methodology = True
        fly_charge = True
        file_type = "xyz"
        data ="" 
        charge =""
        file_type = self.file_type
        coordenadas=str(splitext(self.file)[0])+'.'+file_type

        logFile = open_file(self.file)
       
        
        g=open(coordenadas,'w')
        
        
        
        matchTar=[]
        for i in range(len(logFile)):
            if fly_methodology:
                if "#" in logFile[i]:
                    methodology = logFile[i]
                    if file_type == "com":
                        data = logFile[i-4:i-2]
                    fly_methodology = False
            if fly_charge and file_type=="com": 
                if 'Charge' in logFile[i]:
                    charge = logFile[i]
                    fly_charge = False
                    
            if ('Standard orientation:' in logFile[i]):
                matchTar.append(i)
        
        start=matchTar[-1]+5
        
        for j in range(start,len(logFile)):
            if ('----------------' in logFile[j]):
                end=j
                break
        def words():
            for m in logFile[start:end]:
                words = m.split()
                word1 = int(words[1])
                word1 = elements.get(word1)
                
                print(word1,m[30:-1],file=g)
        
        string = methodology.strip()
        
        if file_type == "com":
            data_str = "{}\n{}\n{}".format(data[0].strip(), data[1].strip(), methodology.strip())
            charge = charge.split()
            charge_str ="\nComents\n\n{} {}".format(charge[2].strip() , charge[5].strip())
            print(data_str, file =g)
            print(charge_str, file=g)
            words()
            print("", file=g)    
        else:
            print(end-start,file=g)
            print('{}'.format(string), file=g)
            words()
        print()
        print('¡¡¡ Se recomeinda comprobar la estructura !!! \n')   
        print(string)
        
        g.close()
            
class HomoLumo():
    def __init__(self, file):
        self.file = open_file(file)
        self.homo_alpha = 0
        self.lumo_alpha = 0
        self.homoHartrees_alpha = 0
        self.lumoHartrees_alpha = 0
        self.homo_beta = 0 
        self.lumo_beta = 0
        self.homoHartrees_beta = 0
        self.lumoHartrees_beta = 0
        
        self.alphaGap = 0
        self.betaGap = 0
        self.generalGap = 0
    
    def calculate(self):
        lista = self.file
        impair = False
        i=0
        fly_electrons = True
        line_electrons = 1
        while (('Optimization completed' in lista[i]) == False):
            
            
            if(fly_electrons and 'alpha electrons' in lista[i]):
              
                line_electrons = i 
               
                
            
            if i == len(lista)-1: 
                i=0
                break
            else:
                i += 1

        line_electrons = lista[line_electrons].split()
        while ('Alpha virt. eigenvalues --' in lista[i]) == False:
            i += 1
            
        endOcc=i-1
        startVirt=i

        if line_electrons[0] != line_electrons[3]:
            while ('Beta virt. eigenvalues --' in lista[i]) == False:
                i += 1
            impair = True

        #print(lista[endOcc], lista[startVirt],sep='\n')


        self.homoHartrees_alpha= eval(lista[endOcc].split()[-1])
        self.lumoHartrees_alpha=eval(lista[startVirt].split()[4])

        self.homo_alpha=self.homoHartrees_alpha*27.2114
        self.lumo_alpha=self.lumoHartrees_alpha*27.2114

        self.alphaGap = abs(self.homo_alpha-self.lumo_alpha)

      

        if(impair):
            endOcc_beta=i-1
            startVirt_beta=i
            self.homoHartrees_beta= eval(lista[endOcc_beta].split()[-1])
            self.lumoHartrees_beta= eval(lista[startVirt_beta].split()[4])
            self.homo_beta=self.homoHartrees_beta*27.2114
            self.lumo_beta=self.lumoHartrees_beta*27.2114
            
            
            
            self.betaGap = abs(self.homo_beta - self.lumo_beta)
            self.generalGap =abs( min(self.lumo_alpha, self.lumo_beta) - max(self.homo_alpha,self.homo_beta ))
            
    def Show(self):
        data_string_alpha = """LUMO(Hartress) Alpha =  {} \t LUMO(eV) Alpha = {}
        HOMO(Hartress) Alpha =  {} \t HOMO(eV) Alpha = {}""".format(self.lumoHartrees_alpha,
           round(self.lumo_alpha,5), self.homoHartrees_alpha,  round(self.homo_alpha,5))
        cal_string_alpha = "SHOMO(Alpha)-SLOMO(Alpha) = {} (eV)".format(round(self.alphaGap, 4))
        data_string_beta = """\nLUMO(Hartress) Beta  =  {} \t LUMO(eV) Beta  = {}
        HOMO(Hartress) Beta  =  {} \t HOMO(eV) Beta  = {}""".format(self.lumoHartrees_beta,
        round(self.lumo_beta,5), self.homoHartrees_beta,  round(self.homo_beta,5))
    
        data_string_alpha += data_string_beta
        cal_string_beta= "\nSHOMO(Beta)-SLOMO(Beta)   = {} (eV)\nSHOMO-SLOMO = {} (eV)".format(round(self.betaGap, 4),round(self.generalGap, 4))
        cal_string_alpha += cal_string_beta
        
        return data_string_alpha +"\n" +cal_string_alpha
        
        
        
        
        
            
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        