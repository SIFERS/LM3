#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 13:23:20 2022

@author: zncg
"""

import matplotlib.pyplot as plt


labels=['molecula','otra molecula','prueba','algo mas','molecula final','La que sea']
accep = [6.5,6.9,6.5,6.9,7.8,4.7]
donor = [4.2,4.5,4.6,3.5,2.1,3.5]


''' 
A partir de aquí no se necesita cambiar nada
'''


plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["New Century Schoolbook"]})


xmin = min(accep)-0.2
xmax = max(accep)+0.2
ymin = min(donor)-0.2
ymax = max(donor)+0.2
markers=["o","v","^","<",">","s","p","P","*","X","1","2","3","4"]

for i in range(len(accep)):
    plt.scatter(accep[i],donor[i],label=labels[i],marker=markers[i])

plt.axhline(y = (ymin+ymax)/2, color = 'k', linestyle = '--' )
plt.axvline(x = (xmin+xmax)/2, color = 'k', linestyle = '--' )

plt.xlabel(r'$\omega^+$ (eV)',size=20)
plt.ylabel(r'$\omega^-$ (eV)',size=20)

plt.legend(bbox_to_anchor=(1.35, 1))
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.grid()
plt.show()



