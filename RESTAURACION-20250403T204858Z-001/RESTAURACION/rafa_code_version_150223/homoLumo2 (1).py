#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 22:11:36 2021

@author: Cisneros-García 
"""
from sys import argv

archivoLog=argv[1]

f=open(archivoLog,'r')

lista=f.readlines()

# esto es para saber donde inician los orbirales de la molecula optimizada
i=0
while ('Optimization completed.' in lista[i]) == False:
    i += 1



#while ('Alpha  occ. eigenvalues --' in lista[i]) == False:
#    i += 1

#startOcc=i


while ('Alpha virt. eigenvalues --' in lista[i]) == False:
    i += 1

endOcc=i-1
startVirt=i


#print(lista[endOcc], lista[startVirt],sep='\n')

homoHartrees= eval(lista[endOcc].split()[-1])
lumoHartrees=eval(lista[startVirt].split()[4])

homo=homoHartrees*27.2114
lumo=lumoHartrees*27.2114

print('---'*10,archivoLog,'---'*10)
print('HOMO(Hartress) = ', homoHartrees, '\t', 'HOMO(eV) = ', round(homo,5) )
print('LUMO(Hartress) = ', lumoHartrees, '\t', 'LUMO(eV) = ', round(lumo,5) )
print('\t\t\t\t','Gap(L-H) = ',round(lumo - homo,5))




    


