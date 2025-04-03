#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 22:11:36 2021

@author: Cisneros-García 
"""

from sys import argv
from os.path import splitext

fly_methodology = True
fly_charge = True
file_type = "xyz"
data ="" 
charge =""

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


archivoLog=argv[1]

f=open(archivoLog,'r')

coordenadas=str(splitext(archivoLog)[0])+'.'+file_type

g=open(coordenadas,'w')

logFile=f.readlines()

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
f.close()
g.close()

