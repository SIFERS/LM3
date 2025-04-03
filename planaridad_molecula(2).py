# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

f = open("y18-Cl-simplif-HSE-TD-6311G.xyz", "r")
print(f.read())

f=open('y18-Cl-simplif-HSE-TD-6311G.xyz','r')
datos=f.readlines()




atom, x,y,z = [],[],[], []

for i in range(len(datos)):
    coords = datos[i].split()
    atom.append(coords[0])
    x.append(float(coords[1]))
    y.append(float(coords[2]))
    z.append(float(coords[3]))

f.close()

'''
x=[0,2,2.5,1,4,7]
y=[0,1,2,3,6,2]
z=[5,10,9,0,3,27]
'''

Xdata = np.column_stack((x, y))

from sklearn import linear_model
reg = linear_model.LinearRegression().fit(Xdata, z)
a0=reg.intercept_
a1, a2 = reg.coef_


maya_x=np.linspace(min(x),max(x),10)
maya_y=np.linspace(min(y),max(y),10)

xx1, yy1 = np.meshgrid(maya_x,maya_y)

xx,yy = np.meshgrid(x,y)

Z = a0+a1*xx+a2*yy
Z1= a0+a1*xx1+a2*yy1

'''
Calculo de los d's
'''
d = []
for i in range(len(x)):
    di = (a0+a1*x[i]+a2*y[i]-z[i])/((a1**2+a2**2+1)**(0.5))
    d.append(di)

d2= []
for j in range(len(d)):
    d2.append(d[j]**2)
 

MPP= np.sqrt((1/len(x))*sum(d2))
print('MPP = ',round(MPP,5))
print('SDP = ', round(max(d)-min(d),5))


fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')

def set_color(_atom,index):
    value_color= dict
    value_color = {"C":"r"}
    if(_atom[index] in value_color):
         return value_color[_atom[index]]
   

for k in range(len(x)):

    color= set_color(atom,k)

    ax.scatter(x[k],y[k],z[k],color =color) # plot the point (2,3,4) on the figure
    ax.text(x[k], y[k], z[k], '%s' % (atom[k]), size=10, zorder=1, color='k')
'''
ax.scatter(x,y,z)
#ax.plot_surface(xx, yy, Z, color='g', alpha=0.1)
ax.plot_wireframe(xx1, yy1, Z1, color='b', alpha=0.3)
ax.set_xlabel('coordenada X')
ax.set_ylabel('cooodenada Y')
ax.set_zlabel('coordenada Z')
#ax.grid(False)
'''
plt.show()
